from asyncio.windows_events import NULL
from decimal import Decimal
from django.forms import ValidationError
from django.db.models import F

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from api.models import Bond
from api.serializers import BondSerializer
import requests
from django.contrib.auth.models import User
from api.serializers import UserSerializer

# Create your views here.


@api_view(["GET"])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getBonds(request):
    try:
        bonds = Bond.objects.all()
        serializer = BondSerializer(bonds, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return JsonResponse({"details": str(e)}, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getBond(request, pk):
    try:
        bond = Bond.objects.get(id=pk)
        if not bond:
            raise Exception("Bond not found")
        serializer = BondSerializer(bond, many=False)
        return Response(serializer.data, status=200)
    except Bond.DoesNotExist:
        return JsonResponse({"details": "Bond with given id not found"}, status=404)
    except Exception as e:
        return JsonResponse({"details": str(e)}, status=401)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createBond(request):
    try:
        data = request.data
        MUTABLE = ["name", "numberOfBonds", "price"]
        if not all(key in MUTABLE for key in request.data.keys()):
            raise Exception("You can only set name, number of bonds and price.")
        bond = Bond.objects.create(
            name=data.get("name"),
            numberOfBonds=data.get("numberOfBonds"),
            price=data.get("price"),
            publishedBy=request.user,
            isPurchased="available",
        )
        bond.save()
        serializer = BondSerializer(bond, many=False)
        return Response(serializer.data, status=201)
    except Exception as e:
        return JsonResponse({"details": str(e)}, status=400)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def buyBond(request, pk):
    try:
        bond = Bond.objects.get(id=pk)
        # Already purchased bond cannot be repurchased
        if bond.isPurchased == "available":
            bond.isPurchased = "purchased"
            bond.purchasedBy = request.user
            bond.save()
        else:
            raise Exception("Invalid Operation")
        serializer = BondSerializer(bond, many=False)
        return Response(serializer.data, status=200)
    except Bond.DoesNotExist:
        return JsonResponse({"details": "Bond with given id not found"}, status=404)
    except Exception as e:
        return JsonResponse({"details": str(e)}, status=403)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def editBond(request, pk):
    try:
        bond = Bond.objects.get(id=pk)
        # Already purchased bond cannot be edited
        if bond.isPurchased == "purchased":
            status = 403
            raise Exception("Bond is already purchased.")
        # Only owner can edit the bond
        if bond.publishedBy == request.user:
            data = request.data
            MUTABLE = ["name", "numberOfBonds", "price"]
            if not all(key in MUTABLE for key in request.data.keys()):
                status = 400
                raise Exception("You can only edit name, number of bonds and price.")
            for key, value in data.items():
                setattr(bond, key, value)
            bond.priceInUSD = None
            bond.save()
        else:
            status = 403
            raise Exception("Permission Denied")
        return Response(BondSerializer(bond, many=False).data, status=200)
    except Bond.DoesNotExist:
        return JsonResponse({"details": "Bond with given id not found"}, status=404)
    except Exception as e:
        return JsonResponse({"details": str(e)}, status=status)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteBond(request, pk):
    try:
        bond = Bond.objects.get(id=pk)
        # Purchased bond cannot be deleted
        if bond.isPurchased == "purchased":
            status = 403
            raise Exception("Bond is already purchased.")
        # Only owner can delete the bond
        if bond.publishedBy == request.user:
            bond.delete()
        else:
            status = 403
            raise Exception("Permission Denied")
        return Response(BondSerializer(bond, many=False).data, status=200)
    except Bond.DoesNotExist:
        return JsonResponse({"details": "Bond with given id not found"}, status=404)
    except Exception as e:
        return JsonResponse({"details": str(e)}, status=status)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def viewInUSD(request):
    try:
        r = requests.get(
            "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno",
            headers={
                "Bmx-Token": "d7f3d87fcc2d208389dee545ce6c9c3a5791c64f0019a40f29df1f3dfedc11f8"
            },
        )
        rate = Decimal(r.json()["bmx"]["series"][0]["datos"][0]["dato"])
        bonds = Bond.objects.all()
        Bond.objects.all().update(priceInUSD=F("price") / rate)
        serializer = BondSerializer(bonds, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return JsonResponse({"details": str(e)}, status=401)
