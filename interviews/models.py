from django.conf import settings
from django.db import models

from core.models import BaseModel


class Interview(BaseModel):
    """An AI-powered interview session for a candidate."""

    class Difficulty(models.TextChoices):
        EASY = "easy", "Easy"
        MEDIUM = "medium", "Medium"
        HARD = "hard", "Hard"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        RUNNING = "running", "Running"
        FINISHED = "finished", "Finished"

    candidate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="interviews",
    )
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100, verbose_name="interview category")
    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.MEDIUM,
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "interview"
        verbose_name_plural = "interviews"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} — {self.candidate.username} ({self.get_status_display()})"


class Question(models.Model):
    """A single question within an interview."""

    class QuestionType(models.TextChoices):
        MCQ = "mcq", "MCQ"
        TEXT = "text", "Text"
        CODING = "coding", "Coding"

    interview = models.ForeignKey(
        Interview,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    question_text = models.TextField()
    question_type = models.CharField(
        max_length=10,
        choices=QuestionType.choices,
        default=QuestionType.TEXT,
    )
    points = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order of the question within the interview",
    )

    class Meta:
        verbose_name = "question"
        verbose_name_plural = "questions"
        ordering = ["order"]

    def __str__(self):
        return f"Q{self.order}: {self.question_text[:50]}"


class Answer(models.Model):
    """A candidate's answer to an interview question."""

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    candidate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    answer_text = models.TextField(blank=True)
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="AI-evaluated score for this answer",
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "answer"
        verbose_name_plural = "answers"
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"Answer by {self.candidate.username} to Q{self.question.order}"


class Result(models.Model):
    """Aggregated result of a completed interview."""

    interview = models.OneToOneField(
        Interview,
        on_delete=models.CASCADE,
        related_name="result",
    )
    total_questions = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text="Overall interview score (percentage or points)",
    )
    feedback = models.TextField(
        blank=True,
        help_text="AI-generated feedback summary",
    )
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "result"
        verbose_name_plural = "results"

    def __str__(self):
        return f"Result for {self.interview.title} — {self.score}"
