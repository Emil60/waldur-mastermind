from enum import Enum


class RoleEnum:
    CUSTOMER_OWNER = 'CUSTOMER.OWNER'
    CUSTOMER_SUPPORT = 'CUSTOMER.SUPPORT'
    CUSTOMER_MANAGER = 'CUSTOMER.MANAGER'

    PROJECT_ADMIN = 'PROJECT.ADMIN'
    PROJECT_MANAGER = 'PROJECT.MANAGER'
    PROJECT_MEMBER = 'PROJECT.MEMBER'

    OFFERING_MANAGER = 'OFFERING.MANAGER'


class PermissionEnum(str, Enum):
    REGISTER_SERVICE_PROVIDER = 'SERVICE_PROVIDER.REGISTER'

    CREATE_OFFERING = 'OFFERING.CREATE'
    DELETE_OFFERING = 'OFFERING.DELETE'
    UPDATE_OFFERING_THUMBNAIL = 'OFFERING.UPDATE_THUMBNAIL'
    UPDATE_OFFERING = 'OFFERING.UPDATE'
    UPDATE_OFFERING_ATTRIBUTES = 'OFFERING.UPDATE_ATTRIBUTES'
    UPDATE_OFFERING_LOCATION = 'OFFERING.UPDATE_LOCATION'
    UPDATE_OFFERING_DESCRIPTION = 'OFFERING.UPDATE_DESCRIPTION'
    UPDATE_OFFERING_OVERVIEW = 'OFFERING.UPDATE_OVERVIEW'
    UPDATE_OFFERING_OPTIONS = 'OFFERING.UPDATE_OPTIONS'
    UPDATE_OFFERING_SECRET_OPTIONS = 'OFFERING.UPDATE_SECRET_OPTIONS'
    ADD_OFFERING_ENDPOINT = 'OFFERING.ADD_ENDPOINT'
    DELETE_OFFERING_ENDPOINT = 'OFFERING.DELETE_ENDPOINT'
    UPDATE_OFFERING_COMPONENTS = 'OFFERING.UPDATE_COMPONENTS'
    PAUSE_OFFERING = 'OFFERING.PAUSE'
    UNPAUSE_OFFERING = 'OFFERING.UNPAUSE'
    ARCHIVE_OFFERING = 'OFFERING.ARCHIVE'
    DRY_RUN_OFFERING_SCRIPT = 'OFFERING.DRY_RUN_SCRIPT'
    MANAGE_CAMPAIGN = 'OFFERING.MANAGE_CAMPAIGN'
    MANAGE_OFFERING_USER_GROUP = 'OFFERING.MANAGE_USER_GROUP'
    CREATE_OFFERING_PLAN = 'OFFERING.CREATE_PLAN'
    UPDATE_OFFERING_PLAN = 'OFFERING.UPDATE_PLAN'
    ARCHIVE_OFFERING_PLAN = 'OFFERING.ARCHIVE_PLAN'
    CREATE_OFFERING_SCREENSHOT = 'OFFERING.CREATE_SCREENSHOT'
    UPDATE_OFFERING_SCREENSHOT = 'OFFERING.UPDATE_SCREENSHOT'
    DELETE_OFFERING_SCREENSHOT = 'OFFERING.DELETE_SCREENSHOT'
    CREATE_OFFERING_USER = 'OFFERING.CREATE_USER'
    CREATE_RESOURCE_ROBOT_ACCOUNT = 'RESOURCE.CREATE_ROBOT_ACCOUNT'
    UPDATE_RESOURCE_ROBOT_ACCOUNT = 'RESOURCE.UPDATE_ROBOT_ACCOUNT'
    DELETE_RESOURCE_ROBOT_ACCOUNT = 'RESOURCE.DELETE_ROBOT_ACCOUNT'

    APPROVE_ORDER = 'ORDER.APPROVE'
    APPROVE_PRIVATE_ORDER = 'ORDER.APPROVE_PRIVATE'
    REJECT_ORDER = 'ORDER.REJECT'

    APPROVE_ORDER_ITEM = 'ORDER_ITEM.APPROVE'
    REJECT_ORDER_ITEM = 'ORDER_ITEM.REJECT'
    DESTROY_ORDER_ITEM = 'ORDER_ITEM.DESTROY'
    TERMINATE_ORDER_ITEM = 'ORDER_ITEM.TERMINATE'

    TERMINATE_RESOURCE = 'RESOURCE.TERMINATE'
    LIST_IMPORTABLE_RESOURCES = 'RESOURCE.LIST_IMPORTABLE'
    SET_RESOURCE_END_DATE = 'RESOURCE.SET_END_DATE'
    SET_RESOURCE_USAGE = 'RESOURCE.SET_USAGE'
    SWITCH_RESOURCE_PLAN = 'RESOURCE.SET_PLAN'
    UPDATE_RESOURCE_LIMITS = 'RESOURCE.SET_LIMITS'
    SET_RESOURCE_BACKEND_ID = 'RESOURCE.SET_BACKEND_ID'
    SUBMIT_RESOURCE_REPORT = 'RESOURCE.SUBMIT_REPORT'
    LIST_RESOURCE_USERS = 'RESOURCE.LIST_USERS'
    COMPLETE_RESOURCE_DOWNSCALING = 'RESOURCE.COMPLETE_DOWNSCALING'
    ACCEPT_BOOKING_REQUEST = 'RESOURCE.ACCEPT_BOOKING_REQUEST'
    REJECT_BOOKING_REQUEST = 'RESOURCE.REJECT_BOOKING_REQUEST'
