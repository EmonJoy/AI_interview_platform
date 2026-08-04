from django.conf import settings
from django.db import models

from core.models import BaseModel


class Resume(BaseModel):
    """Uploaded resume (PDF) linked to a candidate."""

    candidate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="resumes",
    )
    title = models.CharField(max_length=255, verbose_name="resume title")
    pdf = models.FileField(upload_to="resumes/", verbose_name="PDF file")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "resume"
        verbose_name_plural = "resumes"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.title} — {self.candidate.username}"
