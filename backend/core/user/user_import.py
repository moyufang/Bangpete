from fastapi import Depends, FastAPI, Request, Response
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable
from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from contextlib import asynccontextmanager
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from datetime import datetime
import os
from typing import Optional, Any, Union, Dict
from pydantic import BaseModel

from configuration import *
