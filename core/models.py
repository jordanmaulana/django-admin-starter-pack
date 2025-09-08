from bson import objectid
from django.contrib.auth.models import User
from django.db import models


def make_object_id():
    """Generate a unique ObjectId string for use as a model identifier.
    
    Returns:
        str: A unique ObjectId string
    """
    return str(objectid.ObjectId())


class BaseModel(models.Model):
    """
    Abstract base model that provides common fields for all models.
    
    This model includes:
    - uid: Unique identifier using MongoDB ObjectId format
    - created_on: Timestamp when the record was created
    - updated_on: Timestamp when the record was last updated
    - actor: Reference to the user who created/modified the record
    
    All models inheriting from this base will have these common fields
    and consistent behavior across the application.
    """
    
    uid = models.CharField(
        default=make_object_id,
        db_index=True,
        max_length=32,
        verbose_name="Unique Identifier",
        help_text="Unique identifier for this record using ObjectId format"
    )
    
    created_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created On",
        help_text="Timestamp when this record was first created"
    )
    
    updated_on = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated On",
        help_text="Timestamp when this record was last modified"
    )
    
    actor = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Actor",
        help_text="User who created or last modified this record"
    )

    class Meta:
        abstract = True
        ordering = ["-uid"]
        indexes = [models.Index(fields=["created_on"])]
        verbose_name = "Base Model"
        verbose_name_plural = "Base Models"

    def __str__(self):
        """Return string representation of the model.
        
        Returns:
            str: The unique identifier of the record
        """
        return self.uid
