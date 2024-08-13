"""
Module Initialization for API Routers.

This module imports and initializes the API routers for different components of the application.

Routers:
- token: Handles endpoints related to token generation and validation.
- user: Manages user-related endpoints.
- st: Manages endpoints related to Security Targets (ST).
- evaluate: Handles endpoints for evaluating Security Targets and generating evaluation reports.
"""

from router import token, user, st, evaluate

token = token.router
user = user.router
st = st.router
evaluate = evaluate.router
