from django.db import models

from shortuuid.django_fields import ShortUUIDField

from doctor import models as doctor_models
from patient import models as patient_models

class Service(models.Model):
    image=models.FileField(upload_to="images" ,null=True,blank=True )
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    cost = models.DecimalField(max_digits=10,decimal_places=2)
    available_doctors = models.ManyToManyField(doctor_models.Doctor,blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.cost}"
    

class Appointment(models.Model):
    STATUS=[
        ("Scheduled","Scheduled"),
        ("Completed", "completed"),
        ("pending","pending"),
        ("cancelled","cancelled"),
    ]
    
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True,related_name="service_appointment")
    doctor = models.ForeignKey(doctor_models.Doctor, on_delete=models.SET_NULL, null=True, blank=True,related_name="doctor_appointment")
    patient = models.ForeignKey(patient_models.Patient, on_delete=models.SET_NULL, null=True, blank=True,related_name="patient_appointment")
    appointment_date = models.DateTimeField(null=True, blank=True)
    issues = models.TextField(blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    appointment_id = ShortUUIDField(unique=True, length=8,max_length=10,alphabet="123456789", prefix="APT")
    status = models.CharField(max_length=20,choices=STATUS)
    
    def __str__(self):
        return f"{self.patient.full_name} with {self.doctor.full_name}"
    
class MedicalRecord(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField(blank=True, null=True)
    prescriptions = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Medical Record for {self.appointment}"
    
class LabTest(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=255)
    results = models.TextField(blank=True, null=True)
    date_conducted = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.test_name} for {self.appointment}"
    
class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    instructions = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.medication_name} for {self.appointment}"
    
class Billing(models.Model):
    patient = models.ForeignKey(patient_models.Patient, on_delete=models.SET_NULL, null=True, blank=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE,related_name="billing",blank=True,null=True)
    sub_total = models.DecimalField(max_digits=10,decimal_places=2)
    total = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=120,choices=[("Paid","Paid"),("Unpaid","Unpaid"),("Pending","Pending")])
    billing_id = ShortUUIDField(length=6,max_length=10,alphabet="123456789", prefix="BIL")
    
    date = models.DataTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Billing for {self.patient.full_name} - Total:{self.total}"