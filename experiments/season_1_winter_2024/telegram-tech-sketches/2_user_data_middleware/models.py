from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    """User model for storing user information."""
    user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    timezone: Optional[str] = "UTC"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_active: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def full_name(self) -> str:
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.username or str(self.user_id)

    def merge_with(self, other: 'User') -> bool:
        """
        Merge another user's data into this one.
        Returns True if merge was successful, False if there were conflicts.
        """
        # Update non-None values
        for field in self.model_fields:
            other_value = getattr(other, field)
            if other_value is not None:
                current_value = getattr(self, field)
                if current_value is None or field in ['last_active', 'username', 'first_name', 'last_name']:
                    setattr(self, field, other_value)
                elif current_value != other_value and field not in ['user_id', 'created_at']:
                    # Conflict in meaningful data
                    return False
        return True
