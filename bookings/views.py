from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Member, Inventory, Bookings, MAX_BOOKINGS
from rest_framework import status
from .serializers import BookingsSerializer, MemberSerializer, InventorySerializer
import csv
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.generics import ListAPIView


class UploadCSVFileView(APIView):
    def post(self, request, file_type):
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        file_path = default_storage.save(file.name, ContentFile(file.read()))

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            if file_type == "members":
                for row in reader:
                    Member.objects.create(
                        name=row['name'],
                        surname=row['surname'],
                        booking_count=int(row['booking_count']),
                        date_joined=row['date_joined']
                    )
            elif file_type == "inventory":
                for row in reader:
                    Inventory.objects.create(
                        title=row['title'],
                        description=row['description'],
                        remaining_count=int(row['remaining_count']),
                        expiration_date=row['expiration_date']
                    )
            else:
                return JsonResponse({"error": "Invalid file type."}, status=400)

        return JsonResponse({"message": f"{file_type} uploaded successfully."}, status=201)


class BookItemView(APIView):
    def post(self, request):
        member_id = request.data.get("member_id", None)
        inventory_id = request.data.get("inventory_id", None)

        try:
            member = Member.objects.get(id=member_id)
            inventory = Inventory.objects.get(id=inventory_id)

            if member.booking_count >= MAX_BOOKINGS:
                return Response({"error": "Member has reached maximum number of bookings."},
                                status=status.HTTP_400_BAD_REQUEST)

            if inventory.remaining_count <= 0:
                return Response({"error": "Item out of stocks"},
                                status=status.HTTP_400_BAD_REQUEST)

            booking = Bookings.objects.create(member=member, inventory=inventory)

            # Update counts
            member.booking_count += 1
            inventory.remaining_count -= 1
            member.save()
            inventory.save()

            # Serialize and return response
            serializer = BookingsSerializer(booking)
            print(serializer.data)  # Debugging step
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Member.DoesNotExist:
            return Response({"error": "Member not found."}, status=status.HTTP_404_NOT_FOUND)
        except Inventory.DoesNotExist:
            return Response({"error": "Inventory item not found."}, status=status.HTTP_404_NOT_FOUND)


class CancelBookingView(APIView):
    def post(self, request):

        # fetching data from the user or request
        reference = request.data.get("reference")

        try:
            booking = Bookings.objects.get(reference=reference)
            member = booking.member
            inventory = booking.inventory

            member.booking_count -= 1
            inventory.remaining_count += 1
            member.save()
            inventory.save()
            booking.delete()

            return Response({"message": "Booking canceled successfully"}, status=status.HTTP_200_OK)

        except Bookings.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)


class MemberListview(ListAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class InventoeyListView(ListAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer