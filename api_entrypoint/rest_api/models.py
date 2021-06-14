from django.db import models


class Trip(models.Model):
    hash_value = models.CharField("Hash Value", max_length=32)
    region = models.CharField("Region", max_length=256)
    origin_coord = models.CharField("Origin Coordenates", max_length=46)
    destination_coord = models.CharField("Destination Coordenates",
                                         max_length=46)
    date_time = models.DateTimeField("Date Time")
    datasource = models.CharField("Data Source", max_length=256)

    # For data integrity
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", auto_now=True)

    WAITING = "W"
    PROCESSING = "P"
    PROCESSED_SUCCESS = "S"
    PROCESSED_ERROR = "E"
    STATUS_CHOICES = (
        (WAITING, "Waiting"),
        (PROCESSING, "Processing"),
        (PROCESSED_SUCCESS, "Processed - Success"),
        (PROCESSED_ERROR, "Processed - Error"),
    )
    status = models.CharField("Status", max_length=1,
                              default=WAITING, choices=STATUS_CHOICES)

    class Meta:
        verbose_name = "Trip"
        verbose_name_plural = "Trips"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"ID: {self.pk} | Region: {self.region} | DateTime: {self.date_time} | Source: {self.datasource}"
