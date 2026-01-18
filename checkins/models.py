from django.db import models

class CheckIn(models.Model):
    date = models.DateField()
    weight_lb = models.DecimalField(max_digits=5, decimal_places=1)
    bodyfat_percent = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    muscle_lb = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    waist_in = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    chest_in = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    hips_in = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    biceps_in = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    thigh_in = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    calf_in = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} - {self.weight_lb} lb"
