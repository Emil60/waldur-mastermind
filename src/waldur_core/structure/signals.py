from django.dispatch import Signal

# Role related signals
# sender = structure class, e.g. Customer or Project

# providing_args=['structure', 'user', 'role', 'created_by', 'expiration_time']
structure_role_granted = Signal()

# providing_args=['structure', 'user', 'role', 'removed_by']
structure_role_revoked = Signal()

# providing_args=['instance', 'user']
structure_role_updated = Signal()

# providing_args=['instance', 'plan', 'offering']
resource_imported = Signal()

# providing_args=['project', 'old_customer', 'new_customer']
project_moved = Signal()

# providing_args=['permission', 'structure']
permissions_request_approved = Signal()
