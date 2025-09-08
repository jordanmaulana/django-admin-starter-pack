import uuid

from django.db import models

from core.models import BaseModel


class Profile(BaseModel):
    """
    User profile model that extends the BaseModel.
    
    This model represents a user profile with additional information
    beyond the standard Django User model. It includes:
    - name: Display name for the profile
    - deleted_on: Soft deletion timestamp for data retention
    
    The model supports soft deletion functionality and email obfuscation
    for privacy compliance when profiles are marked as deleted.
    """
    
    name = models.CharField(
        max_length=255,
        verbose_name="Profile Name",
        help_text="Display name for this profile (max 255 characters)"
    )
    
    deleted_on = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Deleted On",
        help_text="Timestamp when this profile was soft-deleted. Null if profile is active."
    )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ["-created_on"]

    def obfuscate_email(self):
        """
        Obfuscate the associated user's email and username for privacy.
        
        This method is typically called when a profile is being soft-deleted
        to comply with privacy regulations. It replaces the user's username
        and email with randomized values while preserving the record structure.
        
        Note:
            This method only works if the profile has an associated actor (User).
        """
        if self.actor:
            self.actor.username = f"deleted_{uuid.uuid4()}"
            self.actor.email = f"deleted_{uuid.uuid4()}@example.com"
            self.actor.save()

    def __str__(self):
        """
        Return string representation of the profile.
        
        Returns:
            str: The profile name
        """
        return self.name
