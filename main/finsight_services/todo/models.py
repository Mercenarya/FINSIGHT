from django.db import models
from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    DateTimeField,
    FloatField
)

# USER
class User(Document):
    username = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)
    role = StringField(required=True)

# ADMIN
class Admin(Document):
    user_id = ReferenceField(User, required=True)
    permission_level = StringField(required=True)

# FINANCIAL EXPERT
class FinancialExpert(Document):
    user_id = ReferenceField(User, required=True)
    expertise_field = StringField(required=True)

# DOMAIN KNOWLEDGE
class DomainKnowledge(Document):
    expert_id = ReferenceField(FinancialExpert, required=True)
    topic = StringField(required=True)
    last_update = DateTimeField()

# AI MODEL
class AIModel(Document):
    name = StringField(required=True)
    version = StringField(required=True)
    created_at = DateTimeField()
    description = StringField()

# AI PERFORMANCE METRIC
class AIPerformanceMetric(Document):
    ai_model_id = ReferenceField(AIModel, required=True)
    metric_name = StringField(required=True)
    metric_value = FloatField(required=True)

# DATA SOURCE
class DataSource(Document):
    name = StringField(required=True)
    type = StringField(required=True)
    created_at = DateTimeField()
    url = StringField()
    description = StringField()
    update_date = DateTimeField()
    update_type = StringField()


# DATASET
class Dataset(Document):
    data_source_id = ReferenceField(DataSource, required=True)
    upload_date = DateTimeField()
    status = StringField()


# ANALYSIS REQUEST
class AnalysisRequest(Document):
    user_id = ReferenceField(User, required=True)
    dataset_id = ReferenceField(Dataset, required=True)
    ai_model_id = ReferenceField(AIModel, required=True)
    request_date = DateTimeField()
    status = StringField(required=True)


# REPORT
class Report(Document):
    request_id = ReferenceField(AnalysisRequest, required=True)
    generated_date = DateTimeField()
    summary = StringField()

# FORECAST
class Forecast(Document):
    request_id = ReferenceField(AnalysisRequest, required=True)
    predicted_value = FloatField(required=True)
    confidence_interval = FloatField(required=True)

# AI EVALUATION REQUEST
class Request(Document):
    user_id = ReferenceField(User, required=True)
    ai_model_id = ReferenceField(AIModel, required=True)
    score = FloatField(required=True)
    validated_by = ReferenceField(User)

# HISTORY
class History(Document):
    request_id = ReferenceField(Request, required=True)
    output = StringField()