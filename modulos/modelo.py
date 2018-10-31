# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Index, Integer, SmallInteger, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from sqlalchemy.dialects.mysql.enumerated import ENUM
from sqlalchemy.dialects.mysql.types import LONGBLOB, MEDIUMBLOB
from modulos.base import Base

metadata = Base.metadata

class ActivityLog(Base):
    __tablename__ = 'activity_logs'

    id = Column(Integer, primary_key=True)
    type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    type_id = Column(Integer)
    field = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    action_taker_id = Column(Integer)
    action_taker_type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    initial_value = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    final_value = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    is_created = Column(Integer, nullable=False)
    is_updated = Column(Integer, nullable=False)
    is_deleted = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class AgentTypeRelation(Base):
    __tablename__ = 'agent_type_relations'

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, nullable=False)
    agent_id = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class ApiSetting(Base):
    __tablename__ = 'api_settings'

    id = Column(Integer, primary_key=True)
    key = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Approval(Base):
    __tablename__ = 'approval'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class ApprovalMeta(Base):
    __tablename__ = 'approval_metas'

    id = Column(Integer, primary_key=True)
    approval_id = Column(Integer, nullable=False)
    ticket_id = Column(Integer)
    option = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Banlist(Base):
    __tablename__ = 'banlist'

    id = Column(Integer, primary_key=True)
    ban_status = Column(Integer, nullable=False)
    email_address = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    internal_notes = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class BarNotification(Base):
    __tablename__ = 'bar_notifications'

    id = Column(Integer, primary_key=True)
    key = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class BillType(Base):
    __tablename__ = 'bill_type'

    id = Column(Integer, primary_key=True)
    type = Column(Integer, nullable=False)
    price = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Bill(Base):
    __tablename__ = 'bills'

    id = Column(Integer, primary_key=True)
    level = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    model_id = Column(Integer, nullable=False)
    agent = Column(Integer, nullable=False)
    ticket_id = Column(Integer, nullable=False)
    hours = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    billable = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    amount_hourly = Column(String(255, 'utf8_unicode_ci'))
    note = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class BusinessHoliday(Base):
    __tablename__ = 'business_holidays'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    date = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    business_hours_id = Column(ForeignKey('business_hours.id'), nullable=False, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    business_hours = relationship('BusinessHour', primaryjoin='BusinessHoliday.business_hours_id == BusinessHour.id', backref='business_holidays')


class BusinessHour(Base):
    __tablename__ = 'business_hours'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False)
    timezone = Column(String(255, 'utf8_unicode_ci'))
    is_default = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class BusinessOpenCustomTime(Base):
    __tablename__ = 'business_open_custom_time'

    id = Column(Integer, primary_key=True)
    business_schedule_id = Column(ForeignKey('business_schedule.id'), nullable=False, index=True)
    open_time = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    close_time = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    business_schedule = relationship('BusinessSchedule', primaryjoin='BusinessOpenCustomTime.business_schedule_id == BusinessSchedule.id', backref='business_open_custom_times')


class BusinessSchedule(Base):
    __tablename__ = 'business_schedule'

    id = Column(Integer, primary_key=True)
    business_hours_id = Column(ForeignKey('business_hours.id'), nullable=False, index=True)
    days = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    business_hours = relationship('BusinessHour', primaryjoin='BusinessSchedule.business_hours_id == BusinessHour.id', backref='business_schedules')


class CannedResponse(Base):
    __tablename__ = 'canned_response'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    title = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    message = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    user = relationship('User', primaryjoin='CannedResponse.user_id == User.id', backref='canned_responses')


class Chat(Base):
    __tablename__ = 'chat'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    short = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class CommonSetting(Base):
    __tablename__ = 'common_settings'

    id = Column(Integer, primary_key=True)
    option_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    option_value = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    optional_field = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Condition(Base):
    __tablename__ = 'conditions'

    id = Column(Integer, primary_key=True)
    job = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class CountryCode(Base):
    __tablename__ = 'country_code'

    id = Column(Integer, primary_key=True)
    iso = Column(String(2, 'utf8_unicode_ci'), nullable=False)
    name = Column(String(100, 'utf8_unicode_ci'), nullable=False)
    nicename = Column(String(100, 'utf8_unicode_ci'), nullable=False)
    iso3 = Column(String(3, 'utf8_unicode_ci'), nullable=False)
    numcode = Column(SmallInteger, nullable=False)
    phonecode = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    example = Column(String(255, 'utf8_unicode_ci'), nullable=False)


class CustomForm(Base):
    __tablename__ = 'custom_forms'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))


class Customj(Base):
    __tablename__ = 'customjs'

    id = Column(Integer, primary_key=True)
    name = Column(String(50, 'utf8_unicode_ci'), nullable=False)
    parameter = Column(String(50, 'utf8_unicode_ci'), nullable=False)
    fired_at = Column(String(50, 'utf8_unicode_ci'), nullable=False, server_default=FetchedValue())
    script = Column(String(collation='utf8_unicode_ci'), nullable=False)
    fire = Column(Integer, nullable=False, server_default=FetchedValue())
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class DateFormat(Base):
    __tablename__ = 'date_format'

    id = Column(Integer, primary_key=True)
    format = Column(String(255, 'utf8_unicode_ci'), nullable=False)


class DateTimeFormat(Base):
    __tablename__ = 'date_time_format'

    id = Column(Integer, primary_key=True)
    format = Column(String(255, 'utf8_unicode_ci'), nullable=False)


class Department(Base):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    manager = Column(ForeignKey('users.id'), index=True)
    ticket_assignment = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    outgoing_email = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    template_set = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    auto_ticket_response = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    auto_message_response = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    auto_response_email = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    recipient = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    group_access = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    department_sign = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    business_hour = Column(Integer, nullable=False)
    nodes = Column(String(collation='utf8_unicode_ci'))
    en_auto_assign = Column(Integer, nullable=False, server_default=FetchedValue())

    user = relationship('User', primaryjoin='Department.manager == User.id', backref='departments')


class DepartmentAssignAgent(Base):
    __tablename__ = 'department_assign_agents'

    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, nullable=False)
    agent_id = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class DepartmentAssignManager(Base):
    __tablename__ = 'department_assign_manager'

    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, nullable=False)
    manager_id = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class DepartmentCannedResposne(Base):
    __tablename__ = 'department_canned_resposne'

    id = Column(Integer, primary_key=True)
    dept_id = Column(ForeignKey('department.id'), nullable=False, index=True)
    canned_id = Column(ForeignKey('canned_response.id'), nullable=False, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    canned = relationship('CannedResponse', primaryjoin='DepartmentCannedResposne.canned_id == CannedResponse.id', backref='department_canned_resposnes')
    dept = relationship('Department', primaryjoin='DepartmentCannedResposne.dept_id == Department.id', backref='department_canned_resposnes')


class EmailThread(Base):
    __tablename__ = 'email_threads'

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, nullable=False)
    thread_id = Column(Integer, nullable=False)
    message_id = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    uid = Column(Integer, nullable=False)
    reference_id = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    fetching_email = Column(String(255, 'utf8_unicode_ci'), nullable=False)


class Email(Base):
    __tablename__ = 'emails'
    __table_args__ = (
        Index('department', 'department', 'priority', 'help_topic'),
        Index('department_2', 'department', 'priority', 'help_topic')
    )

    id = Column(Integer, primary_key=True)
    email_address = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    email_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    department = Column(ForeignKey('department.id'))
    priority = Column(ForeignKey('ticket_priority.priority_id'), index=True)
    help_topic = Column(ForeignKey('help_topic.id'), index=True)
    user_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    password = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    fetching_host = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    fetching_port = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    fetching_protocol = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    fetching_encryption = Column(String(255, 'utf8_unicode_ci'))
    mailbox_protocol = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    imap_config = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    folder = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    sending_host = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    sending_port = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    sending_protocol = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    sending_encryption = Column(String(255, 'utf8_unicode_ci'))
    smtp_validate = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    smtp_authentication = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    internal_notes = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    auto_response = Column(Integer, nullable=False)
    fetching_status = Column(Integer, nullable=False)
    move_to_folder = Column(Integer, nullable=False)
    delete_email = Column(Integer, nullable=False)
    do_nothing = Column(Integer, nullable=False)
    sending_status = Column(Integer, nullable=False)
    authentication = Column(Integer, nullable=False)
    header_spoofing = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    block_auto_generated = Column(Integer, nullable=False, server_default=FetchedValue())
    domain = Column(String(255, 'utf8_unicode_ci'))
    key = Column(String(255, 'utf8_unicode_ci'))
    secret = Column(String(255, 'utf8_unicode_ci'))
    region = Column(String(255, 'utf8_unicode_ci'))

    department1 = relationship('Department', primaryjoin='Email.department == Department.id', backref='emails')
    help_topic1 = relationship('HelpTopic', primaryjoin='Email.help_topic == HelpTopic.id', backref='emails')
    ticket_priority = relationship('TicketPriority', primaryjoin='Email.priority == TicketPriority.priority_id', backref='emails')


class ExtraOrg(Base):
    __tablename__ = 'extra_orgs'

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, nullable=False)
    key = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class FailedJob(Base):
    __tablename__ = 'failed_jobs'

    id = Column(Integer, primary_key=True)
    connection = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    queue = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    payload = Column(String(collation='utf8_unicode_ci'), nullable=False)
    exception = Column(String(collation='utf8_unicode_ci'), nullable=False)
    failed_at = Column(DateTime, nullable=False, server_default=FetchedValue())


class FaveoMail(Base):
    __tablename__ = 'faveo_mails'

    id = Column(Integer, primary_key=True)
    email_id = Column(Integer, nullable=False)
    drive = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    key = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class FaveoQueue(Base):
    __tablename__ = 'faveo_queues'

    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, nullable=False)
    key = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Filter(Base):
    __tablename__ = 'filters'

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, nullable=False)
    key = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Followup(Base):
    __tablename__ = 'followup'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    condition = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Form(Base):
    __tablename__ = 'forms'

    id = Column(Integer, primary_key=True)
    form = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    json = Column(String(collation='utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class GroupAssignDepartment(Base):
    __tablename__ = 'group_assign_department'

    id = Column(Integer, primary_key=True)
    group_id = Column(ForeignKey('groups.id'), nullable=False, index=True)
    department_id = Column(ForeignKey('department.id'), nullable=False, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    department = relationship('Department', primaryjoin='GroupAssignDepartment.department_id == Department.id', backref='group_assign_departments')
    group = relationship('Group', primaryjoin='GroupAssignDepartment.group_id == Group.id', backref='group_assign_departments')


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(50, 'latin1_spanish_ci'))


class Halt(Base):
    __tablename__ = 'halts'

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, nullable=False)
    halted_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    time_used = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    halted_time = Column(Integer)


class HelpTopic(Base):
    __tablename__ = 'help_topic'

    id = Column(Integer, primary_key=True)
    topic = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    parent_topic = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    custom_form = Column(ForeignKey('custom_forms.id'), index=True)
    department = Column(ForeignKey('department.id'), index=True)
    ticket_status = Column(ForeignKey('ticket_status.id'), index=True)
    thank_page = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    ticket_num_format = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    internal_notes = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    auto_response = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    nodes = Column(String(collation='utf8_unicode_ci'))
    linked_departments = Column(String(5000, 'utf8_unicode_ci'))

    custom_form1 = relationship('CustomForm', primaryjoin='HelpTopic.custom_form == CustomForm.id', backref='help_topics')
    department1 = relationship('Department', primaryjoin='HelpTopic.department == Department.id', backref='help_topics')
    ticket_statu = relationship('TicketStatu', primaryjoin='HelpTopic.ticket_status == TicketStatu.id', backref='help_topics')


class HelptopicAssignType(Base):
    __tablename__ = 'helptopic_assign_type'

    id = Column(Integer, primary_key=True)
    helptopic_id = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    type_id = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class InAppPushNotification(Base):
    __tablename__ = 'in_app_push_notifications'

    id = Column(Integer, primary_key=True)
    subscribed_user_id = Column(Integer, nullable=False)
    message = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    url = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(ENUM('pending', 'failed', 'delivered'), nullable=False, server_default=FetchedValue())
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Job(Base):
    __tablename__ = 'jobs'
    __table_args__ = (
        Index('jobs_queue_reserved_at_index', 'queue', 'reserved_at'),
    )

    id = Column(BigInteger, primary_key=True)
    queue = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    payload = Column(String(collation='utf8_unicode_ci'), nullable=False)
    attempts = Column(Integer, nullable=False)
    reserved_at = Column(Integer)
    available_at = Column(Integer, nullable=False)
    created_at = Column(Integer, nullable=False)


class KbArticle(Base):
    __tablename__ = 'kb_article'

    id = Column(Integer, primary_key=True)
    name = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    slug = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    publish_time = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    template = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    seo_title = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    meta_description = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    visible_to = Column(String(255, 'utf8_unicode_ci'), server_default=FetchedValue())
    author = Column(Integer, server_default=FetchedValue())


class KbArticleRelationship(Base):
    __tablename__ = 'kb_article_relationship'

    id = Column(Integer, primary_key=True)
    article_id = Column(ForeignKey('kb_article.id'), nullable=False, index=True)
    category_id = Column(ForeignKey('kb_category.id'), nullable=False, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    article = relationship('KbArticle', primaryjoin='KbArticleRelationship.article_id == KbArticle.id', backref='kb_article_relationships')
    category = relationship('KbCategory', primaryjoin='KbArticleRelationship.category_id == KbCategory.id', backref='kb_article_relationships')


class KbArticleTemplate(Base):
    __tablename__ = 'kb_article_template'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False)
    description = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class KbCategory(Base):
    __tablename__ = 'kb_category'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    slug = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False)
    parent = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    display_order = Column(Integer, nullable=False)


class KbComment(Base):
    __tablename__ = 'kb_comment'

    id = Column(Integer, primary_key=True)
    article_id = Column(ForeignKey('kb_article.id'), nullable=False, index=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    email = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    website = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    comment = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    profile_pic = Column(String(255, 'utf8_unicode_ci'))

    article = relationship('KbArticle', primaryjoin='KbComment.article_id == KbArticle.id', backref='kb_comments')


class KbPage(Base):
    __tablename__ = 'kb_pages'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False)
    visibility = Column(Integer, nullable=False)
    slug = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    seo_title = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    meta_description = Column(String(255, 'utf8_unicode_ci'), nullable=False)


class KbSetting(Base):
    __tablename__ = 'kb_settings'

    id = Column(Integer, primary_key=True)
    pagination = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    status = Column(Integer, nullable=False)
    date_format = Column(String(255, 'utf8_unicode_ci'), nullable=False, server_default=FetchedValue())


class Label(Base):
    __tablename__ = 'labels'

    id = Column(Integer, primary_key=True)
    title = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    color = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    order = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    visible_to = Column(Text(collation='utf8_unicode_ci'))


class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    locale = Column(String(255, 'utf8_unicode_ci'), nullable=False)


class Ldap(Base):
    __tablename__ = 'ldap'

    id = Column(Integer, primary_key=True)
    domain = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    username = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    password = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    search_base = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    agent_auth = Column(Integer, nullable=False)
    client_auth = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_valid = Column(Integer, nullable=False, server_default=FetchedValue())


class LdapSearchBase(Base):
    __tablename__ = 'ldap_search_bases'

    id = Column(Integer, primary_key=True)
    ldap_id = Column(Integer, nullable=False)
    search_base = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    user_type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    department_ids = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    organization_ids = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class License(Base):
    __tablename__ = 'licenses'

    id = Column(Integer, primary_key=True)
    licenses_type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    org_id = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    licenses_key = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    activated_on = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    start_date = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    expires_on = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    comments = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class LimeSurvey(Base):
    __tablename__ = 'lime_survey'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    survey_link = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class ListenerAction(Base):
    __tablename__ = 'listener_actions'

    id = Column(Integer, primary_key=True)
    listener_id = Column(Integer, nullable=False)
    key = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    meta = Column(String(collation='utf8_unicode_ci'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    custom_action = Column(String(collation='utf8_unicode_ci'))


class ListenerEvent(Base):
    __tablename__ = 'listener_events'

    id = Column(Integer, primary_key=True)
    listener_id = Column(Integer, nullable=False)
    event = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    condition = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    old = Column(String(255, 'utf8_unicode_ci'))
    new = Column(String(255, 'utf8_unicode_ci'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class ListenerRule(Base):
    __tablename__ = 'listener_rules'

    id = Column(Integer, primary_key=True)
    listener_id = Column(Integer, nullable=False)
    key = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    condition = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(String(255, 'utf8_unicode_ci'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    custom_rule = Column(String(collation='utf8_unicode_ci'))


class Listener(Base):
    __tablename__ = 'listeners'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False)
    description = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    performed_by = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    order = Column(Integer, nullable=False)
    rule_match = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    title = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    email = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    phone = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    address = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class LoginAttempt(Base):
    __tablename__ = 'login_attempts'

    id = Column(Integer, primary_key=True)
    User = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    IP = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    Attempts = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    LastLogin = Column(DateTime, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class MailService(Base):
    __tablename__ = 'mail_services'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    short_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class MailboxProtocol(Base):
    __tablename__ = 'mailbox_protocol'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(String(50, 'utf8_unicode_ci'))


class Migration(Base):
    __tablename__ = 'migrations'

    id = Column(Integer, primary_key=True)
    migration = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    batch = Column(Integer, nullable=False)


class NoAssignEscalate(Base):
    __tablename__ = 'no_assign_escalate'

    id = Column(Integer, primary_key=True)
    sla_plan = Column(Integer, nullable=False)
    escalate_time = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    escalate_type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    escalate_person = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    message = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    by = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    to = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    seen = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    table = Column(String(255, 'utf8_unicode_ci'))
    row_id = Column(Integer)
    url = Column(String(255, 'utf8_unicode_ci'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class OrgAttachment(Base):
    __tablename__ = 'org_attachment'

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, nullable=False)
    file_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Organization(Base):
    __tablename__ = 'organization'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    phone = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    website = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    address = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    head = Column(ForeignKey('users.id'), index=True)
    internal_notes = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    client_Code = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    phone1 = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    line_of_business = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    relation_type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    branch = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    fax = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    logo = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    domain = Column(String(255, 'utf8_unicode_ci'), nullable=False)

    user = relationship('User', primaryjoin='Organization.head == User.id', backref='organizations')


class OrganizationDept(Base):
    __tablename__ = 'organization_dept'

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, nullable=False)
    org_deptname = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    business_hours_id = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    org_dept_manager = Column(Text(collation='utf8_unicode_ci'))


t_password_resets = Table(
    'password_resets', metadata,
    Column('email', String(255, 'utf8_unicode_ci'), nullable=False, index=True),
    Column('token', String(255, 'utf8_unicode_ci'), nullable=False, index=True),
    Column('created_at', DateTime, nullable=False, server_default=FetchedValue())
)


class Permision(Base):
    __tablename__ = 'permision'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    permision = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Plugin(Base):
    __tablename__ = 'plugins'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    path = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class ProSerialKey(Base):
    __tablename__ = 'pro_serial_key'

    id = Column(Integer, primary_key=True)
    order_id = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    serial_key = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class QueueService(Base):
    __tablename__ = 'queue_services'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    short_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class RatingRef(Base):
    __tablename__ = 'rating_ref'

    id = Column(Integer, primary_key=True)
    rating_id = Column(Integer, nullable=False)
    ticket_id = Column(Integer, nullable=False)
    thread_id = Column(Integer, nullable=False)
    rating_value = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    display_order = Column(Integer, nullable=False)
    allow_modification = Column(Integer, nullable=False)
    rating_scale = Column(Integer, nullable=False)
    rating_area = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    restrict = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class RecureContent(Base):
    __tablename__ = 'recure_contents'

    id = Column(Integer, primary_key=True)
    recur_id = Column(Integer, nullable=False)
    option = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(String(collation='utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Recur(Base):
    __tablename__ = 'recurs'

    id = Column(Integer, primary_key=True)
    interval = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    delivery_on = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    last_execution = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Report(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True)
    file = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    type = Column(String(100, 'utf8_unicode_ci'), nullable=False)
    hash = Column(String(100, 'utf8_unicode_ci'), nullable=False, unique=True)
    expired_at = Column(DateTime, nullable=False)
    user_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class RequiredField(Base):
    __tablename__ = 'required_fields'

    id = Column(Integer, primary_key=True)
    form = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    is_agent_required = Column(Integer, nullable=False)
    is_client_required = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Required(Base):
    __tablename__ = 'requireds'

    id = Column(Integer, primary_key=True)
    form = Column(String(255, 'utf8_unicode_ci'))
    field = Column(String(255, 'utf8_unicode_ci'))
    agent = Column(String(255, 'utf8_unicode_ci'))
    client = Column(String(255, 'utf8_unicode_ci'))
    parent = Column(Integer)
    option = Column(String(255, 'utf8_unicode_ci'))
    label = Column(String(255, 'utf8_unicode_ci'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Reseller(Base):
    __tablename__ = 'reseller'

    id = Column(Integer, primary_key=True)
    userid = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    apikey = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    mode = Column(Integer, nullable=False)
    enforce = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SdAttachmentType(Base):
    __tablename__ = 'sd_attachment_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SdAttachment(Base):
    __tablename__ = 'sd_attachments'

    id = Column(Integer, primary_key=True)
    saved = Column(ForeignKey('sd_attachment_types.id'), nullable=False, index=True)
    owner = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    size = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    sd_attachment_type = relationship('SdAttachmentType', primaryjoin='SdAttachment.saved == SdAttachmentType.id', backref='sd_attachments')


class SdCab(Base):
    __tablename__ = 'sd_cab'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    head = Column(ForeignKey('users.id'), index=True)
    approvers = Column(String(255, 'utf8_unicode_ci'))
    aproval_mandatory = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    user = relationship('User', primaryjoin='SdCab.head == User.id', backref='sd_cabs')


class SdCabVote(Base):
    __tablename__ = 'sd_cab_votes'

    id = Column(Integer, primary_key=True)
    cab_id = Column(ForeignKey('sd_cab.id'), index=True)
    user_id = Column(ForeignKey('users.id'), index=True)
    comment = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    owner = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    vote = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    cab = relationship('SdCab', primaryjoin='SdCabVote.cab_id == SdCab.id', backref='sd_cab_votes')
    user = relationship('User', primaryjoin='SdCabVote.user_id == User.id', backref='sd_cab_votes')


class SdChangePriority(Base):
    __tablename__ = 'sd_change_priorities'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SdChangeRelease(Base):
    __tablename__ = 'sd_change_release'

    id = Column(Integer, primary_key=True)
    change_id = Column(ForeignKey('sd_changes.id'), index=True)
    release_id = Column(ForeignKey('sd_releases.id'), index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    change = relationship('SdChange', primaryjoin='SdChangeRelease.change_id == SdChange.id', backref='sd_change_releases')
    release = relationship('SdRelease', primaryjoin='SdChangeRelease.release_id == SdRelease.id', backref='sd_change_releases')


class SdChangeStatu(Base):
    __tablename__ = 'sd_change_status'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SdChangeType(Base):
    __tablename__ = 'sd_change_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SdChange(Base):
    __tablename__ = 'sd_changes'

    id = Column(Integer, primary_key=True)
    description = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    subject = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    requester = Column(ForeignKey('users.id'), index=True)
    status_id = Column(ForeignKey('sd_change_status.id'), index=True)
    priority_id = Column(ForeignKey('sd_change_priorities.id'), index=True)
    change_type_id = Column(ForeignKey('sd_change_types.id'), index=True)
    impact_id = Column(ForeignKey('sd_impact_types.id'), index=True)
    location_id = Column(Integer)
    approval_id = Column(ForeignKey('sd_cab.id'), index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    approval = relationship('SdCab', primaryjoin='SdChange.approval_id == SdCab.id', backref='sd_changes')
    change_type = relationship('SdChangeType', primaryjoin='SdChange.change_type_id == SdChangeType.id', backref='sd_changes')
    impact = relationship('SdImpactType', primaryjoin='SdChange.impact_id == SdImpactType.id', backref='sd_changes')
    priority = relationship('SdChangePriority', primaryjoin='SdChange.priority_id == SdChangePriority.id', backref='sd_changes')
    user = relationship('User', primaryjoin='SdChange.requester == User.id', backref='sd_changes')
    status = relationship('SdChangeStatu', primaryjoin='SdChange.status_id == SdChangeStatu.id', backref='sd_changes')


class SdGerneral(Base):
    __tablename__ = 'sd_gerneral'

    id = Column(Integer, primary_key=True)
    owner = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    key = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SdImpactType(Base):
    __tablename__ = 'sd_impact_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SdLocationCategory(Base):
    __tablename__ = 'sd_location_categories'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SdLocation(Base):
    __tablename__ = 'sd_locations'

    id = Column(Integer, primary_key=True)
    location_category_id = Column(ForeignKey('sd_location_categories.id'), index=True)
    title = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    organization = Column(Integer)
    email = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    phone = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    address = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    all_department_access = Column(Integer, nullable=False)
    departments = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    location_category = relationship('SdLocationCategory', primaryjoin='SdLocation.location_category_id == SdLocationCategory.id', backref='sd_locations')


class SdProblem(Base):
    __tablename__ = 'sd_problem'

    id = Column(Integer, primary_key=True)
    _from = Column('from', String(255, 'utf8_unicode_ci'), nullable=False)
    subject = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    department = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status_type_id = Column(Integer)
    priority_id = Column(Integer)
    impact_id = Column(Integer)
    location_type_id = Column(Integer)
    group_id = Column(Integer)
    agent_id = Column(Integer)
    assigned_id = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SdProblemChange(Base):
    __tablename__ = 'sd_problem_change'

    id = Column(Integer, primary_key=True)
    problem_id = Column(ForeignKey('sd_problem.id'), index=True)
    change_id = Column(ForeignKey('sd_changes.id'), index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    change = relationship('SdChange', primaryjoin='SdProblemChange.change_id == SdChange.id', backref='sd_problem_changes')
    problem = relationship('SdProblem', primaryjoin='SdProblemChange.problem_id == SdProblem.id', backref='sd_problem_changes')


class SdReleasePriority(Base):
    __tablename__ = 'sd_release_priorities'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SdReleaseStatu(Base):
    __tablename__ = 'sd_release_status'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SdReleaseType(Base):
    __tablename__ = 'sd_release_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SdRelease(Base):
    __tablename__ = 'sd_releases'

    id = Column(Integer, primary_key=True)
    description = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    subject = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    planned_start_date = Column(DateTime)
    planned_end_date = Column(DateTime)
    status_id = Column(ForeignKey('sd_release_status.id'), index=True)
    priority_id = Column(ForeignKey('sd_release_priorities.id'), index=True)
    release_type_id = Column(ForeignKey('sd_release_types.id'), index=True)
    location_id = Column(ForeignKey('sd_locations.id'), index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    location = relationship('SdLocation', primaryjoin='SdRelease.location_id == SdLocation.id', backref='sd_releases')
    priority = relationship('SdReleasePriority', primaryjoin='SdRelease.priority_id == SdReleasePriority.id', backref='sd_releases')
    release_type = relationship('SdReleaseType', primaryjoin='SdRelease.release_type_id == SdReleaseType.id', backref='sd_releases')
    status = relationship('SdReleaseStatu', primaryjoin='SdRelease.status_id == SdReleaseStatu.id', backref='sd_releases')


class SdTicketRelation(Base):
    __tablename__ = 'sd_ticket_relation'

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, nullable=False)
    owner = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SettingsAlertNotice(Base):
    __tablename__ = 'settings_alert_notice'

    id = Column(Integer, primary_key=True)
    key = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SettingsAutoResponse(Base):
    __tablename__ = 'settings_auto_response'

    id = Column(Integer, primary_key=True)
    new_ticket = Column(Integer, nullable=False)
    agent_new_ticket = Column(Integer, nullable=False)
    submitter = Column(Integer, nullable=False)
    participants = Column(Integer, nullable=False)
    overlimit = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SettingsCompany(Base):
    __tablename__ = 'settings_company'

    id = Column(Integer, primary_key=True)
    company_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    website = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    phone = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    address = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    landing_page = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    offline_page = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    thank_page = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    logo = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    use_logo = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SettingsEmail(Base):
    __tablename__ = 'settings_email'

    id = Column(Integer, primary_key=True)
    template = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    sys_email = Column(String(255, 'utf8_unicode_ci'))
    alert_email = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    admin_email = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    mta = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    email_fetching = Column(Integer, nullable=False)
    notification_cron = Column(Integer, nullable=False)
    strip = Column(Integer, nullable=False)
    separator = Column(Integer, nullable=False)
    all_emails = Column(Integer, nullable=False)
    email_collaborator = Column(Integer, nullable=False)
    attachment = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SettingsRating(Base):
    __tablename__ = 'settings_ratings'

    id = Column(Integer, primary_key=True)
    rating_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    publish = Column(Integer, nullable=False)
    modify = Column(Integer, nullable=False)
    slug = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SettingsSecurity(Base):
    __tablename__ = 'settings_security'

    id = Column(Integer, primary_key=True)
    lockout_message = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    backlist_offender = Column(Integer, nullable=False)
    backlist_threshold = Column(Integer, nullable=False)
    lockout_period = Column(Integer, nullable=False)
    days_to_keep_logs = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SettingsSystem(Base):
    __tablename__ = 'settings_system'

    id = Column(Integer, primary_key=True)
    status = Column(Integer, nullable=False)
    url = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    department = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    page_size = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    log_level = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    purge_log = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    api_enable = Column(Integer, nullable=False)
    api_key_mandatory = Column(Integer, nullable=False)
    api_key = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    name_format = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    time_farmat = Column(Integer, index=True)
    date_format = Column(Integer, index=True)
    time_zone = Column(String(50, 'utf8_unicode_ci'))
    date_time_format = Column(String(50, 'utf8_unicode_ci'))
    day_date_time = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    content = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    version = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    serial_key = Column(String(100, 'utf8_unicode_ci'))
    order_number = Column(String(100, 'utf8_unicode_ci'))


class SettingsTicket(Base):
    __tablename__ = 'settings_ticket'

    id = Column(Integer, primary_key=True)
    num_format = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    num_sequence = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    help_topic = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    max_open_ticket = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    collision_avoid = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    lock_ticket_frequency = Column(String(255, 'utf8_unicode_ci'), nullable=False, server_default=FetchedValue())
    captcha = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False)
    claim_response = Column(Integer, nullable=False)
    assigned_ticket = Column(Integer, nullable=False)
    answered_ticket = Column(Integer, nullable=False)
    agent_mask = Column(Integer, nullable=False)
    html = Column(Integer, nullable=False)
    client_update = Column(Integer, nullable=False)
    max_file_size = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    count_internal = Column(Integer, nullable=False, server_default=FetchedValue())
    show_status_date = Column(Integer, nullable=False, server_default=FetchedValue())
    show_org_details = Column(Integer, nullable=False, server_default=FetchedValue())
    custom_field_name = Column(Text(collation='utf8_unicode_ci'))


class SlaApproachEscalate(Base):
    __tablename__ = 'sla_approach_escalate'

    id = Column(Integer, primary_key=True)
    sla_plan = Column(Integer, nullable=False)
    escalate_time = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    escalate_type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    escalate_person = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SlaCustomEnforcement(Base):
    __tablename__ = 'sla_custom_enforcements'

    id = Column(Integer, primary_key=True)
    f_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    f_type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    f_value = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    f_label = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    sla_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SlaPlan(Base):
    __tablename__ = 'sla_plan'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    grace_period = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    admin_note = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False)
    sla_target = Column(Integer, nullable=False)
    apply_sla_depertment = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    apply_sla_company = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    apply_sla_tickettype = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    apply_sla_ticketsource = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    transient = Column(Integer, nullable=False)
    ticket_overdue = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    apply_sla_helptopic = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    apply_sla_orgdepts = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    apply_sla_labels = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    apply_sla_tags = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    order = Column(Integer)
    is_default = Column(Integer, nullable=False, server_default=FetchedValue())


class SlaTarget(Base):
    __tablename__ = 'sla_targets'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    sla_id = Column(Integer, nullable=False)
    priority_id = Column(Integer, nullable=False)
    respond_within = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    resolve_within = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    business_hour_id = Column(Integer, nullable=False)
    send_email = Column(Integer, nullable=False)
    send_sms = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    in_app = Column(Integer)


class SlaViolatedEscalate(Base):
    __tablename__ = 'sla_violated_escalate'

    id = Column(Integer, primary_key=True)
    sla_plan = Column(Integer, nullable=False)
    escalate_time = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    escalate_type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    escalate_person = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Sm(Base):
    __tablename__ = 'sms'

    id = Column(Integer, primary_key=True)
    provider_id = Column(Integer, nullable=False)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SmsServiceProvider(Base):
    __tablename__ = 'sms_service_providers'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SmsTemplateSet(Base):
    __tablename__ = 'sms_template_sets'

    id = Column(Integer, primary_key=True)
    name = Column(String(100, 'utf8_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False, server_default=FetchedValue())
    is_default = Column(Integer, nullable=False, server_default=FetchedValue())
    template_language = Column(String(10, 'utf8_unicode_ci'), nullable=False, server_default=FetchedValue())
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SmsTemplateType(Base):
    __tablename__ = 'sms_template_types'

    id = Column(Integer, primary_key=True)
    type = Column(String(100, 'utf8_unicode_ci'), nullable=False)
    description = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    body = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    event_type = Column(Integer, nullable=False)
    template_category = Column(String(100, 'utf8_unicode_ci'))
    set_id = Column(ForeignKey('sms_template_sets.id'), nullable=False, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    set = relationship('SmsTemplateSet', primaryjoin='SmsTemplateType.set_id == SmsTemplateSet.id', backref='sms_template_types')


class SocialChannel(Base):
    __tablename__ = 'social_channel'

    id = Column(Integer, primary_key=True)
    channel = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    via = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    message_id = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    con_id = Column(String(255, 'utf8_unicode_ci'))
    user_id = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    ticket_id = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    username = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    posted_at = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SocialMedia(Base):
    __tablename__ = 'social_media'

    id = Column(Integer, primary_key=True)
    provider = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    key = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(Text(collation='utf8_unicode_ci'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SubscribedUser(Base):
    __tablename__ = 'subscribed_users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    browser_name = Column(String(90, 'utf8_unicode_ci'), nullable=False)
    version = Column(Integer, nullable=False)
    user_agent = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    platform = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class SystemPortal(Base):
    __tablename__ = 'system_portal'

    id = Column(Integer, primary_key=True)
    admin_header_color = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    agent_header_color = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    client_header_color = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    client_button_color = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    client_button_border_color = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    client_input_fild_color = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    logo = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    icon = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(String(255, 'utf8_unicode_ci'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class TaskAssignee(Base):
    __tablename__ = 'task_assignees'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    team_id = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    task_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    task_description = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    task_start_date = Column(DateTime)
    task_end_date = Column(DateTime)
    created_by = Column(Integer, nullable=False)
    status = Column(ENUM('active', 'inactive', 'deleted'), nullable=False, server_default=FetchedValue())
    is_private = Column(Integer, nullable=False, server_default=FetchedValue())
    ticket_id = Column(Integer)
    parent_id = Column(Integer)
    is_complete = Column(Integer, nullable=False, server_default=FetchedValue())
    due_alert = Column(DateTime, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class TasksAlert(Base):
    __tablename__ = 'tasks_alerts'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, nullable=False)
    repeat_alerts = Column(ENUM('never', 'daily', 'weekly', 'monthly', 'never'), nullable=False, server_default=FetchedValue())
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class TasksThread(Base):
    __tablename__ = 'tasks_threads'

    id = Column(Integer, primary_key=True)
    system_note = Column(Integer, nullable=False, server_default=FetchedValue())
    task_id = Column(Integer, nullable=False)
    message = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    created_by = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class TeamAssignAgent(Base):
    __tablename__ = 'team_assign_agent'

    id = Column(Integer, primary_key=True)
    team_id = Column(ForeignKey('teams.id'), index=True)
    agent_id = Column(ForeignKey('users.id'), index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    agent = relationship('User', primaryjoin='TeamAssignAgent.agent_id == User.id', backref='team_assign_agents')
    team = relationship('Team', primaryjoin='TeamAssignAgent.team_id == Team.id', backref='team_assign_agents')


class TeamAssignDepartment(Base):
    __tablename__ = 'team_assign_department'

    id = Column(Integer, primary_key=True)
    team_id = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    dept_id = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False)
    team_lead = Column(ForeignKey('users.id'), index=True)
    assign_alert = Column(Integer, nullable=False)
    admin_notes = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    user = relationship('User', primaryjoin='Team.team_lead == User.id', backref='teams')


class TelephoneCall(Base):
    __tablename__ = 'telephone_calls'

    id = Column(Integer, primary_key=True)
    callid = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    provider = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    key = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class TelephoneDetail(Base):
    __tablename__ = 'telephone_details'

    id = Column(Integer, primary_key=True)
    provider = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    key = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class TelephoneProvider(Base):
    __tablename__ = 'telephone_providers'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    short = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Template(Base):
    __tablename__ = 'template'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False)
    template_set_to_clone = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    language = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    internal_note = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class TemplateSet(Base):
    __tablename__ = 'template_sets'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    active = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    template_language = Column(String(10, 'utf8_unicode_ci'), server_default=FetchedValue())


class TemplateType(Base):
    __tablename__ = 'template_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Template(Base):
    __tablename__ = 'templates'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    variable = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    type = Column(Integer, nullable=False)
    subject = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    message = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    description = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    set_id = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    template_category = Column(String(100, 'utf8_unicode_ci'))


t_threadview = Table(
    'threadview', metadata,
    Column('ticket_id', Integer),
    Column('thread_type', String(255)),
    Column('textbody', String)
)


class TicketAttachment(Base):
    __tablename__ = 'ticket_attachment'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    thread_id = Column(ForeignKey('ticket_thread.id'), index=True)
    size = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    poster = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    file = Column(MEDIUMBLOB)
    driver = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    path = Column(String(255, 'utf8_unicode_ci'), nullable=False)

    thread = relationship('TicketThread', primaryjoin='TicketAttachment.thread_id == TicketThread.id', backref='ticket_attachments')


class TicketCollaborator(Base):
    __tablename__ = 'ticket_collaborator'

    id = Column(Integer, primary_key=True)
    isactive = Column(Integer, nullable=False)
    ticket_id = Column(ForeignKey('tickets.id'), index=True)
    user_id = Column(ForeignKey('users.id'), index=True)
    role = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    ticket = relationship('Ticket', primaryjoin='TicketCollaborator.ticket_id == Ticket.id', backref='ticket_collaborators')
    user = relationship('User', primaryjoin='TicketCollaborator.user_id == User.id', backref='ticket_collaborators')


class TicketFilterMeta(Base):
    __tablename__ = 'ticket_filter_meta'

    id = Column(Integer, primary_key=True)
    ticket_filter_id = Column(Integer, nullable=False, index=True)
    key = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(String(collation='utf8_unicode_ci'), nullable=False)


class TicketFilterShareable(Base):
    __tablename__ = 'ticket_filter_shareables'

    id = Column(Integer, primary_key=True)
    ticket_filter_id = Column(Integer, nullable=False)
    ticket_filter_shareable_id = Column(Integer, nullable=False)
    ticket_filter_shareable_type = Column(String(255, 'utf8_unicode_ci'), nullable=False)


class TicketFilter(Base):
    __tablename__ = 'ticket_filters'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class TicketFormDatum(Base):
    __tablename__ = 'ticket_form_data'

    id = Column(Integer, primary_key=True)
    ticket_id = Column(ForeignKey('tickets.id'), index=True)
    title = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    content = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    key = Column(String(255, 'utf8_unicode_ci'), nullable=False)

    ticket = relationship('Ticket', primaryjoin='TicketFormDatum.ticket_id == Ticket.id', backref='ticket_form_data')


class TicketPriority(Base):
    __tablename__ = 'ticket_priority'

    priority_id = Column(Integer, primary_key=True)
    priority = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    priority_desc = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    priority_color = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    priority_urgency = Column(Integer, nullable=False)
    ispublic = Column(Integer, nullable=False)
    is_default = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class TicketSource(Base):
    __tablename__ = 'ticket_source'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    css_class = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(String(collation='utf8_unicode_ci'))
    location = Column(String(255, 'utf8_unicode_ci'), nullable=False)


class TicketStatu(Base):
    __tablename__ = 'ticket_status'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    message = Column(LONGBLOB, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    visibility_for_client = Column(Integer, nullable=False)
    allow_client = Column(Integer, nullable=False)
    visibility_for_agent = Column(Integer, nullable=False)
    purpose_of_status = Column(Integer, nullable=False)
    secondary_status = Column(Integer)
    send_email = Column(String(255, 'utf8_unicode_ci'))
    halt_sla = Column(Integer, nullable=False)
    order = Column(Integer, nullable=False)
    icon = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    icon_color = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    default = Column(Integer)
    send_sms = Column(Integer, nullable=False, server_default=FetchedValue())


class TicketStatusOverride(Base):
    __tablename__ = 'ticket_status_override'

    id = Column(Integer, primary_key=True)
    current_status = Column(Integer, nullable=False)
    target_status = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class TicketStatusType(Base):
    __tablename__ = 'ticket_status_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class TicketThread(Base):
    __tablename__ = 'ticket_thread'

    id = Column(Integer, primary_key=True)
    ticket_id = Column(ForeignKey('tickets.id'), index=True)
    user_id = Column(ForeignKey('users.id'), index=True)
    thread_type = Column(String(255, 'utf8_unicode_ci'))
    poster = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    source = Column(ForeignKey('ticket_source.id'), index=True)
    reply_rating = Column(Integer, nullable=False)
    rating_count = Column(Integer, nullable=False)
    is_internal = Column(Integer, nullable=False)
    title = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    body = Column(LONGBLOB)
    format = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    ip_address = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    response_time = Column(String(255, 'utf8_unicode_ci'))

    ticket_source = relationship('TicketSource', primaryjoin='TicketThread.source == TicketSource.id', backref='ticket_threads')
    ticket = relationship('Ticket', primaryjoin='TicketThread.ticket_id == Ticket.id', backref='ticket_threads')
    user = relationship('User', primaryjoin='TicketThread.user_id == User.id', backref='ticket_threads')


class TicketToken(Base):
    __tablename__ = 'ticket_token'

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, nullable=False)
    token = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class TicketType(Base):
    __tablename__ = 'ticket_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False)
    type_desc = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    ispublic = Column(Integer, nullable=False)
    is_default = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    ticket_number = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    user_id = Column(ForeignKey('users.id'), index=True)
    dept_id = Column(ForeignKey('department.id'), index=True)
    team_id = Column(ForeignKey('teams.id'), index=True)
    priority_id = Column(ForeignKey('ticket_priority.priority_id'), index=True)
    sla = Column(ForeignKey('sla_plan.id'), index=True)
    help_topic_id = Column(ForeignKey('help_topic.id'), index=True)
    status = Column(ForeignKey('ticket_status.id'), index=True)
    rating = Column(Integer, nullable=False)
    ratingreply = Column(Integer, nullable=False)
    flags = Column(Integer, nullable=False)
    ip_address = Column(Integer, nullable=False)
    assigned_to = Column(ForeignKey('users.id'), index=True)
    lock_by = Column(Integer, nullable=False)
    lock_at = Column(DateTime)
    source = Column(ForeignKey('ticket_source.id'), index=True)
    isoverdue = Column(Integer, nullable=False)
    reopened = Column(Integer, nullable=False)
    isanswered = Column(Integer, nullable=False)
    html = Column(Integer, nullable=False)
    is_deleted = Column(Integer, nullable=False)
    closed = Column(Integer, nullable=False)
    is_transferred = Column(Integer, nullable=False)
    transferred_at = Column(DateTime, nullable=False)
    reopened_at = Column(DateTime)
    duedate = Column(DateTime)
    closed_at = Column(DateTime)
    last_message_at = Column(DateTime)
    first_response_time = Column(DateTime)
    approval = Column(Integer, nullable=False)
    follow_up = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    resolution_time = Column(String(255, 'utf8_unicode_ci'))
    is_response_sla = Column(Integer, nullable=False)
    is_resolution_sla = Column(Integer, nullable=False)
    type = Column(Integer, index=True)

    user = relationship('User', primaryjoin='Ticket.assigned_to == User.id', backref='user_tickets')
    dept = relationship('Department', primaryjoin='Ticket.dept_id == Department.id', backref='tickets')
    help_topic = relationship('HelpTopic', primaryjoin='Ticket.help_topic_id == HelpTopic.id', backref='tickets')
    priority = relationship('TicketPriority', primaryjoin='Ticket.priority_id == TicketPriority.priority_id', backref='tickets')
    sla_plan = relationship('SlaPlan', primaryjoin='Ticket.sla == SlaPlan.id', backref='tickets')
    ticket_source = relationship('TicketSource', primaryjoin='Ticket.source == TicketSource.id', backref='tickets')
    ticket_statu = relationship('TicketStatu', primaryjoin='Ticket.status == TicketStatu.id', backref='tickets')
    team = relationship('Team', primaryjoin='Ticket.team_id == Team.id', backref='tickets')
    user1 = relationship('User', primaryjoin='Ticket.user_id == User.id', backref='user_tickets_0')


class TimeFormat(Base):
    __tablename__ = 'time_format'

    id = Column(Integer, primary_key=True)
    format = Column(String(255, 'utf8_unicode_ci'), nullable=False)


class TimeTrack(Base):
    __tablename__ = 'time_tracks'

    id = Column(Integer, primary_key=True)
    description = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    work_time = Column(Integer, nullable=False)
    ticket_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Timezone(Base):
    __tablename__ = 'timezone'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    location = Column(String(255, 'utf8_unicode_ci'), nullable=False)


class TypeTopicLink(Base):
    __tablename__ = 'type_topic_link'

    type = Column(Integer, primary_key=True, nullable=False)
    topic = Column(Integer, primary_key=True, nullable=False)


class UserAdditionalInfo(Base):
    __tablename__ = 'user_additional_infos'

    id = Column(Integer, primary_key=True)
    owner = Column(Integer, nullable=False)
    service = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    key = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(String(255, 'utf8_unicode_ci'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class UserAssignOrganization(Base):
    __tablename__ = 'user_assign_organization'

    id = Column(Integer, primary_key=True)
    org_id = Column(ForeignKey('organization.id'), index=True)
    user_id = Column(ForeignKey('users.id'), index=True)
    role = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    org_department = Column(String(255, 'utf8_unicode_ci'))

    org = relationship('Organization', primaryjoin='UserAssignOrganization.org_id == Organization.id', backref='user_assign_organizations')
    user = relationship('User', primaryjoin='UserAssignOrganization.user_id == User.id', backref='user_assign_organizations')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    first_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    last_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    gender = Column(Integer, nullable=False)
    email = Column(String(255, 'utf8_unicode_ci'), unique=True)
    ban = Column(Integer, nullable=False)
    password = Column(String(60, 'utf8_unicode_ci'), nullable=False)
    active = Column(Integer, nullable=False)
    is_delete = Column(Integer, nullable=False)
    ext = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    country_code = Column(Integer, nullable=False)
    phone_number = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    mobile = Column(String(255, 'utf8_unicode_ci'), unique=True)
    agent_sign = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    account_type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    account_status = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    assign_group = Column(ForeignKey('groups.id'), index=True)
    primary_dpt = Column(ForeignKey('department.id'), index=True)
    agent_tzone = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    daylight_save = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    limit_access = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    directory_listing = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    vacation_mode = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    company = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    role = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    internal_note = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    profile_pic = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    remember_token = Column(String(100, 'utf8_unicode_ci'))
    fcm_token = Column(String(255, 'utf8_unicode_ci'))
    i_token = Column(String(255, 'utf8_unicode_ci'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    user_language = Column(String(10, 'utf8_unicode_ci'))
    mobile_otp_verify = Column(String(255, 'utf8_unicode_ci'), nullable=False, server_default=FetchedValue())
    email_verify = Column(String(255, 'utf8_unicode_ci'), nullable=False, server_default=FetchedValue())
    location = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    is_login = Column(Integer, nullable=False)
    not_accept_ticket = Column(Integer, nullable=False)
    ldap_username = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    isldapauth = Column(Integer, nullable=False)
    ldap_guid = Column(String(255, 'utf8_unicode_ci'))

    group = relationship('Group', primaryjoin='User.assign_group == Group.id', backref='users')
    department = relationship('Department', primaryjoin='User.primary_dpt == Department.id', backref='users')


class VersionCheck(Base):
    __tablename__ = 'version_check'

    id = Column(Integer, primary_key=True)
    current_version = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    new_version = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Widget(Base):
    __tablename__ = 'widgets'

    id = Column(Integer, primary_key=True)
    name = Column(String(30, 'utf8_unicode_ci'))
    title = Column(String(50, 'utf8_unicode_ci'))
    value = Column(Text(collation='utf8_unicode_ci'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class WorkflowAction(Base):
    __tablename__ = 'workflow_action'

    id = Column(Integer, primary_key=True)
    workflow_id = Column(ForeignKey('workflow_name.id'), nullable=False, index=True)
    condition = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    action = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    custom_action = Column(String(collation='utf8_unicode_ci'))
    updated_at = Column(DateTime)

    workflow = relationship('WorkflowName', primaryjoin='WorkflowAction.workflow_id == WorkflowName.id', backref='workflow_actions')


class WorkflowClose(Base):
    __tablename__ = 'workflow_close'

    id = Column(Integer, primary_key=True)
    days = Column(Integer, nullable=False)
    condition = Column(Integer, nullable=False)
    send_email = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class WorkflowName(Base):
    __tablename__ = 'workflow_name'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False)
    order = Column(Integer, nullable=False)
    target = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    internal_note = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    rule_match = Column(String(10, 'utf8_unicode_ci'), nullable=False, server_default=FetchedValue())


class WorkflowRule(Base):
    __tablename__ = 'workflow_rules'

    id = Column(Integer, primary_key=True)
    workflow_id = Column(ForeignKey('workflow_name.id'), nullable=False, index=True)
    matching_criteria = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    matching_scenario = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    matching_relation = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    matching_value = Column(Text(collation='utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    custom_rule = Column(String(collation='utf8_unicode_ci'))
    updated_at = Column(DateTime)

    workflow = relationship('WorkflowName', primaryjoin='WorkflowRule.workflow_id == WorkflowName.id', backref='workflow_rules')