class ConstStrings:
# Authentication messages
    INTERNAL_SERVER_ERROR = 'Internal Server Error'
    VALIDATION_ERROR = 'Validation Error'
    USER_REGISTER = 'User Registered successfully!'
    RATE_EXCEEDED = 'Rate exceeded'
    TOO_MANY = 'Too many failed attempts. Try later!'
    LOGIN_SUCCESS = 'Login successful'
    LOGOUT_SUCCESS = 'Logged out successfully'
    USER_EXISTS = 'User already exists'
    NO_USER = 'No registered user!'
    INVALID_PASSWORD = 'Invalid password'
    ACCOUNT_INACTIVE = 'Account is inactive'
    NEW_ACCESS_TOKEN = 'New access token generated'
    TOKEN_REQUIRED = 'Unauthorized. Token is required'
    TOKEN_EXPIRED = 'Token is expired / blacklisted'
    INVALID_TOKEN = 'Invalid or expired token'
    INVALID_REFRESH_TOKEN = 'Invalid refresh token'
    REFRESH_TOKEN_EXPIRED = "Refresh token expired"

# Routes
    GET_POST_ROUTE = ''
    ID_ROUTE = '/{id}'
    AUTH_PREFIX = '/auth'
    AUTH_TAG = 'Authentication'
    REGISTER_ROUTE = '/register'
    LOGIN_ROUTE = '/login'
    REFRESH_TOKEN_ROUTE = '/refresh'
    LOGOUT_ROUTE = '/logout'

    CATEGORY_PREFIX = '/categories'
    CATEGORY_TAG = 'Categories'
    BULK_CATEGORY_ROUTE = '/bulk'

    PRODUCT_PREFIX = '/products'
    PRODUCT_TAG = 'Products'
    BULK_PRODUCT_ROUTE = '/bulk'

# Database Table
    CATEGORIES_TABLE = 'categories'
    PRODUCTS_TABLE = 'products'
    USER_TABLE = 'user'
    BLACKLIST_TOKEN_TABLE = 'blacklisted_tokens'

# Normal Strings
    USER_ID_FIELD = 'user_id'
    TRUE= 'true'
    FALSE = 'false'
    ASCENDING = 'asc'
    DESCENDING = 'desc'
    NO_UPDATE = 'No fields provided for update'
    NO_CHANGE = 'No changes detected'

# Categories message
    CATEGORY_CREATED = 'Category created successfully'
    CATEGORY_FETCHED = 'Categories fetched successfully'
    MULTI_CATEGORY_CREATED = 'Categories created successfully'
    CATEGORY_UPDATED = 'Categories updated successfully'
    CATEGORY_DELETED = 'Categories deleted successfully'
    CATEGORY_NAME_EMPTY = 'Category name cannot be empty'
    CATEGORY_NAME_STRINGS = 'Category name cannot be numeric'
    CATEGORY_EXISTS = 'Category name already exists'
    NO_CATEGORY = 'Category not found'
    INVALID_CATEGORY = 'Invalid category id'

# Products message
    PRODUCT_CREATED = 'Product created successfully'
    PRODUCTS_FETCHED = 'Products fetched successfully'
    MULTI_PRODUCTS_CREATED = 'Products created successfully'
    PRODUCT_UPDATED = 'Product updated successfully'
    PRODUCT_DELETED = 'Product deleted successfully'
    NO_PRODUCT = 'Product not found'
    PRODUCT_NAME_EMPTY = 'Product name cannot be empty'
    PRODUCT_NAME_STRINGS = 'Product name cannot be numeric'
    PRICE_NOT_ZERO = 'Price must be greater than 0'