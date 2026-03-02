from typing import List, Dict, Any, Optional, Union
import pandas as pd
from LimbleConnection.endpoint import LimbleEndpoint

class LimbleConnection(object):
    @property
    def me(self) -> MeNamespace: ...
    @property
    def assets(self) -> AssetsNamespace: ...
    @property
    def locations(self) -> LocationsNamespace: ...
    @property
    def parts(self) -> PartsNamespace: ...
    @property
    def tasks(self) -> TasksNamespace: ...
    @property
    def users(self) -> UsersNamespace: ...
    @property
    def vendors(self) -> VendorsNamespace: ...
    @property
    def roles(self) -> RolesNamespace: ...
    @property
    def teams(self) -> TeamsNamespace: ...
    @property
    def purchase_orders(self) -> Purchase_ordersNamespace: ...
    @property
    def general_ledgers(self) -> General_ledgersNamespace: ...
    @property
    def budgets(self) -> BudgetsNamespace: ...
    @property
    def priorities(self) -> PrioritiesNamespace: ...
    @property
    def tags(self) -> TagsNamespace: ...
    @property
    def statuses(self) -> StatusesNamespace: ...
    @property
    def bills(self) -> BillsNamespace: ...
    @property
    def regions(self) -> RegionsNamespace: ...
    @property
    def webhooks(self) -> WebhooksNamespace: ...
    @property
    def units_of_measure(self) -> Units_of_measureNamespace: ...

class Units_of_measureNamespace(object):
    @property
    def get_units(self) -> Units_of_measureGet_unitsNamespace: ...
    @property
    def create_unit(self) -> Units_of_measureCreate_unitNamespace: ...
    @property
    def update_unit(self) -> Units_of_measureUpdate_unitNamespace: ...

class Units_of_measureUpdate_unitNamespace(LimbleEndpoint):
    pass

class Units_of_measureCreate_unitNamespace(LimbleEndpoint):
    pass

class Units_of_measureGet_unitsNamespace(LimbleEndpoint):
    pass

class WebhooksNamespace(object):
    @property
    def get_webhooks(self) -> WebhooksGet_webhooksNamespace: ...
    @property
    def delete_webhook(self) -> WebhooksDelete_webhookNamespace: ...
    @property
    def new_webhook(self) -> WebhooksNew_webhookNamespace: ...
    @property
    def update_webhook(self) -> WebhooksUpdate_webhookNamespace: ...

class WebhooksUpdate_webhookNamespace(LimbleEndpoint):
    pass

class WebhooksNew_webhookNamespace(LimbleEndpoint):
    pass

class WebhooksDelete_webhookNamespace(LimbleEndpoint):
    pass

class WebhooksGet_webhooksNamespace(LimbleEndpoint):
    pass

class RegionsNamespace(LimbleEndpoint):
    @property
    def create_region(self) -> RegionsCreate_regionNamespace: ...
    @property
    def update_region(self) -> RegionsUpdate_regionNamespace: ...
    @property
    def delete_region(self) -> RegionsDelete_regionNamespace: ...

class RegionsDelete_regionNamespace(LimbleEndpoint):
    pass

class RegionsUpdate_regionNamespace(LimbleEndpoint):
    pass

class RegionsCreate_regionNamespace(LimbleEndpoint):
    pass

class BillsNamespace(object):
    @property
    def transactions(self) -> BillsTransactionsNamespace: ...
    @property
    def comments(self) -> BillsCommentsNamespace: ...
    @property
    def get_bills(self) -> BillsGet_billsNamespace: ...
    @property
    def new_bill(self) -> BillsNew_billNamespace: ...
    @property
    def update_bill(self) -> BillsUpdate_billNamespace: ...
    @property
    def delete_bill(self) -> BillsDelete_billNamespace: ...

class BillsDelete_billNamespace(LimbleEndpoint):
    pass

class BillsUpdate_billNamespace(LimbleEndpoint):
    pass

class BillsNew_billNamespace(LimbleEndpoint):
    pass

class BillsGet_billsNamespace(LimbleEndpoint):
    pass

class BillsCommentsNamespace(object):
    @property
    def bill_comments(self) -> BillsCommentsBill_commentsNamespace: ...
    @property
    def create_bill_comment(self) -> BillsCommentsCreate_bill_commentNamespace: ...
    @property
    def upload_bill_comment_file(self) -> BillsCommentsUpload_bill_comment_fileNamespace: ...
    @property
    def delete_bill_comment_file(self) -> BillsCommentsDelete_bill_comment_fileNamespace: ...
    @property
    def delete_bill_comment(self) -> BillsCommentsDelete_bill_commentNamespace: ...

class BillsCommentsDelete_bill_commentNamespace(LimbleEndpoint):
    pass

class BillsCommentsDelete_bill_comment_fileNamespace(LimbleEndpoint):
    pass

class BillsCommentsUpload_bill_comment_fileNamespace(LimbleEndpoint):
    pass

class BillsCommentsCreate_bill_commentNamespace(LimbleEndpoint):
    pass

class BillsCommentsBill_commentsNamespace(LimbleEndpoint):
    pass

class BillsTransactionsNamespace(object):
    @property
    def add_bill_item(self) -> BillsTransactionsAdd_bill_itemNamespace: ...
    @property
    def bill_transactions(self) -> BillsTransactionsBill_transactionsNamespace: ...
    @property
    def update_bill_transaction(self) -> BillsTransactionsUpdate_bill_transactionNamespace: ...
    @property
    def bill_transaction(self) -> BillsTransactionsBill_transactionNamespace: ...

class BillsTransactionsBill_transactionNamespace(LimbleEndpoint):
    pass

class BillsTransactionsUpdate_bill_transactionNamespace(LimbleEndpoint):
    pass

class BillsTransactionsBill_transactionsNamespace(LimbleEndpoint):
    pass

class BillsTransactionsAdd_bill_itemNamespace(LimbleEndpoint):
    pass

class StatusesNamespace(LimbleEndpoint):
    @property
    def create_status(self) -> StatusesCreate_statusNamespace: ...
    @property
    def update_status(self) -> StatusesUpdate_statusNamespace: ...
    @property
    def delete_status(self) -> StatusesDelete_statusNamespace: ...

class StatusesDelete_statusNamespace(LimbleEndpoint):
    pass

class StatusesUpdate_statusNamespace(LimbleEndpoint):
    pass

class StatusesCreate_statusNamespace(LimbleEndpoint):
    pass

class TagsNamespace(object):
    @property
    def get_tags(self) -> TagsGet_tagsNamespace: ...
    @property
    def create_account_tag(self) -> TagsCreate_account_tagNamespace: ...
    @property
    def rename_account_tag(self) -> TagsRename_account_tagNamespace: ...
    @property
    def delete_account_tag(self) -> TagsDelete_account_tagNamespace: ...

class TagsDelete_account_tagNamespace(LimbleEndpoint):
    pass

class TagsRename_account_tagNamespace(LimbleEndpoint):
    pass

class TagsCreate_account_tagNamespace(LimbleEndpoint):
    pass

class TagsGet_tagsNamespace(LimbleEndpoint):
    pass

class PrioritiesNamespace(object):
    @property
    def get_priorities(self) -> PrioritiesGet_prioritiesNamespace: ...
    @property
    def update_priority(self) -> PrioritiesUpdate_priorityNamespace: ...
    @property
    def new_priority(self) -> PrioritiesNew_priorityNamespace: ...
    @property
    def delete_priority(self) -> PrioritiesDelete_priorityNamespace: ...

class PrioritiesDelete_priorityNamespace(LimbleEndpoint):
    pass

class PrioritiesNew_priorityNamespace(LimbleEndpoint):
    pass

class PrioritiesUpdate_priorityNamespace(LimbleEndpoint):
    pass

class PrioritiesGet_prioritiesNamespace(LimbleEndpoint):
    pass

class BudgetsNamespace(object):
    @property
    def steps(self) -> BudgetsStepsNamespace: ...
    @property
    def get_budgets(self) -> BudgetsGet_budgetsNamespace: ...
    @property
    def new_budget(self) -> BudgetsNew_budgetNamespace: ...
    @property
    def delete_budget(self) -> BudgetsDelete_budgetNamespace: ...
    @property
    def update_budget(self) -> BudgetsUpdate_budgetNamespace: ...

class BudgetsUpdate_budgetNamespace(LimbleEndpoint):
    pass

class BudgetsDelete_budgetNamespace(LimbleEndpoint):
    pass

class BudgetsNew_budgetNamespace(LimbleEndpoint):
    pass

class BudgetsGet_budgetsNamespace(LimbleEndpoint):
    pass

class BudgetsStepsNamespace(object):
    @property
    def new_step(self) -> BudgetsStepsNew_stepNamespace: ...
    @property
    def delete_step(self) -> BudgetsStepsDelete_stepNamespace: ...
    @property
    def get_steps(self) -> BudgetsStepsGet_stepsNamespace: ...
    @property
    def update_step(self) -> BudgetsStepsUpdate_stepNamespace: ...

class BudgetsStepsUpdate_stepNamespace(LimbleEndpoint):
    pass

class BudgetsStepsGet_stepsNamespace(LimbleEndpoint):
    pass

class BudgetsStepsDelete_stepNamespace(LimbleEndpoint):
    pass

class BudgetsStepsNew_stepNamespace(LimbleEndpoint):
    pass

class General_ledgersNamespace(object):
    @property
    def get_general_ledgers(self) -> General_ledgersGet_general_ledgersNamespace: ...
    @property
    def new_general_ledger(self) -> General_ledgersNew_general_ledgerNamespace: ...
    @property
    def update_general_ledger(self) -> General_ledgersUpdate_general_ledgerNamespace: ...
    @property
    def delete_general_ledger(self) -> General_ledgersDelete_general_ledgerNamespace: ...

class General_ledgersDelete_general_ledgerNamespace(LimbleEndpoint):
    pass

class General_ledgersUpdate_general_ledgerNamespace(LimbleEndpoint):
    pass

class General_ledgersNew_general_ledgerNamespace(LimbleEndpoint):
    pass

class General_ledgersGet_general_ledgersNamespace(LimbleEndpoint):
    pass

class Purchase_ordersNamespace(object):
    @property
    def items(self) -> Purchase_ordersItemsNamespace: ...
    @property
    def comments(self) -> Purchase_ordersCommentsNamespace: ...
    @property
    def state(self) -> Purchase_ordersStateNamespace: ...
    @property
    def get_purchase_orders(self) -> Purchase_ordersGet_purchase_ordersNamespace: ...
    @property
    def new_purchase_order(self) -> Purchase_ordersNew_purchase_orderNamespace: ...
    @property
    def update_purchase_order(self) -> Purchase_ordersUpdate_purchase_orderNamespace: ...
    @property
    def delete_po(self) -> Purchase_ordersDelete_poNamespace: ...

class Purchase_ordersDelete_poNamespace(LimbleEndpoint):
    pass

class Purchase_ordersUpdate_purchase_orderNamespace(LimbleEndpoint):
    pass

class Purchase_ordersNew_purchase_orderNamespace(LimbleEndpoint):
    pass

class Purchase_ordersGet_purchase_ordersNamespace(LimbleEndpoint):
    pass

class Purchase_ordersStateNamespace(object):
    @property
    def change_po_state(self) -> Purchase_ordersStateChange_po_stateNamespace: ...
    @property
    def get_po_state_transitions(self) -> Purchase_ordersStateGet_po_state_transitionsNamespace: ...

class Purchase_ordersStateGet_po_state_transitionsNamespace(LimbleEndpoint):
    pass

class Purchase_ordersStateChange_po_stateNamespace(LimbleEndpoint):
    pass

class Purchase_ordersCommentsNamespace(object):
    @property
    def po_comments(self) -> Purchase_ordersCommentsPo_commentsNamespace: ...
    @property
    def upload_po_comment_file(self) -> Purchase_ordersCommentsUpload_po_comment_fileNamespace: ...
    @property
    def delete_po_comment_file(self) -> Purchase_ordersCommentsDelete_po_comment_fileNamespace: ...
    @property
    def create_po_comment(self) -> Purchase_ordersCommentsCreate_po_commentNamespace: ...
    @property
    def delete_po_comment(self) -> Purchase_ordersCommentsDelete_po_commentNamespace: ...

class Purchase_ordersCommentsDelete_po_commentNamespace(LimbleEndpoint):
    pass

class Purchase_ordersCommentsCreate_po_commentNamespace(LimbleEndpoint):
    pass

class Purchase_ordersCommentsDelete_po_comment_fileNamespace(LimbleEndpoint):
    pass

class Purchase_ordersCommentsUpload_po_comment_fileNamespace(LimbleEndpoint):
    pass

class Purchase_ordersCommentsPo_commentsNamespace(LimbleEndpoint):
    pass

class Purchase_ordersItemsNamespace(object):
    @property
    def get_purchase_order_items(self) -> Purchase_ordersItemsGet_purchase_order_itemsNamespace: ...
    @property
    def new_purchase_order_item(self) -> Purchase_ordersItemsNew_purchase_order_itemNamespace: ...
    @property
    def update_purchase_order_item(self) -> Purchase_ordersItemsUpdate_purchase_order_itemNamespace: ...
    @property
    def delete_po_item(self) -> Purchase_ordersItemsDelete_po_itemNamespace: ...
    @property
    def receive_po_item(self) -> Purchase_ordersItemsReceive_po_itemNamespace: ...

class Purchase_ordersItemsReceive_po_itemNamespace(LimbleEndpoint):
    pass

class Purchase_ordersItemsDelete_po_itemNamespace(LimbleEndpoint):
    pass

class Purchase_ordersItemsUpdate_purchase_order_itemNamespace(LimbleEndpoint):
    pass

class Purchase_ordersItemsNew_purchase_order_itemNamespace(LimbleEndpoint):
    pass

class Purchase_ordersItemsGet_purchase_order_itemsNamespace(LimbleEndpoint):
    pass

class TeamsNamespace(object):
    @property
    def get_teams(self) -> TeamsGet_teamsNamespace: ...
    @property
    def create_team(self) -> TeamsCreate_teamNamespace: ...
    @property
    def update_team(self) -> TeamsUpdate_teamNamespace: ...
    @property
    def delete_team(self) -> TeamsDelete_teamNamespace: ...

class TeamsDelete_teamNamespace(LimbleEndpoint):
    pass

class TeamsUpdate_teamNamespace(LimbleEndpoint):
    pass

class TeamsCreate_teamNamespace(LimbleEndpoint):
    pass

class TeamsGet_teamsNamespace(LimbleEndpoint):
    pass

class RolesNamespace(object):
    @property
    def get_roles(self) -> RolesGet_rolesNamespace: ...
    @property
    def create_role(self) -> RolesCreate_roleNamespace: ...
    @property
    def update_role(self) -> RolesUpdate_roleNamespace: ...
    @property
    def delete_role(self) -> RolesDelete_roleNamespace: ...

class RolesDelete_roleNamespace(LimbleEndpoint):
    pass

class RolesUpdate_roleNamespace(LimbleEndpoint):
    pass

class RolesCreate_roleNamespace(LimbleEndpoint):
    pass

class RolesGet_rolesNamespace(LimbleEndpoint):
    pass

class VendorsNamespace(LimbleEndpoint):
    @property
    def fields(self) -> VendorsFieldsNamespace: ...
    @property
    def images(self) -> VendorsImagesNamespace: ...
    @property
    def logs(self) -> VendorsLogsNamespace: ...
    @property
    def new_vendor(self) -> VendorsNew_vendorNamespace: ...
    @property
    def update_vendor(self) -> VendorsUpdate_vendorNamespace: ...
    @property
    def delete_vendor(self) -> VendorsDelete_vendorNamespace: ...

class VendorsDelete_vendorNamespace(LimbleEndpoint):
    pass

class VendorsUpdate_vendorNamespace(LimbleEndpoint):
    pass

class VendorsNew_vendorNamespace(LimbleEndpoint):
    pass

class VendorsLogsNamespace(object):
    @property
    def files(self) -> VendorsLogsFilesNamespace: ...
    @property
    def vendor_logs(self) -> VendorsLogsVendor_logsNamespace: ...
    @property
    def new_vendor_log(self) -> VendorsLogsNew_vendor_logNamespace: ...
    @property
    def update_vendor_log(self) -> VendorsLogsUpdate_vendor_logNamespace: ...
    @property
    def delete_vendor_log(self) -> VendorsLogsDelete_vendor_logNamespace: ...

class VendorsLogsDelete_vendor_logNamespace(LimbleEndpoint):
    pass

class VendorsLogsUpdate_vendor_logNamespace(LimbleEndpoint):
    pass

class VendorsLogsNew_vendor_logNamespace(LimbleEndpoint):
    pass

class VendorsLogsVendor_logsNamespace(LimbleEndpoint):
    pass

class VendorsLogsFilesNamespace(object):
    @property
    def delete_vendor_log_file(self) -> VendorsLogsFilesDelete_vendor_log_fileNamespace: ...
    @property
    def add_vendor_log_file(self) -> VendorsLogsFilesAdd_vendor_log_fileNamespace: ...

class VendorsLogsFilesAdd_vendor_log_fileNamespace(LimbleEndpoint):
    pass

class VendorsLogsFilesDelete_vendor_log_fileNamespace(LimbleEndpoint):
    pass

class VendorsImagesNamespace(object):
    @property
    def add_vendor_image(self) -> VendorsImagesAdd_vendor_imageNamespace: ...
    @property
    def delete_vendor_image(self) -> VendorsImagesDelete_vendor_imageNamespace: ...

class VendorsImagesDelete_vendor_imageNamespace(LimbleEndpoint):
    pass

class VendorsImagesAdd_vendor_imageNamespace(LimbleEndpoint):
    pass

class VendorsFieldsNamespace(object):
    @property
    def vendor_fields(self) -> VendorsFieldsVendor_fieldsNamespace: ...
    @property
    def vendor_suggested_fields(self) -> VendorsFieldsVendor_suggested_fieldsNamespace: ...
    @property
    def update_vendor_field_value(self) -> VendorsFieldsUpdate_vendor_field_valueNamespace: ...
    @property
    def attach_field_to_vendor(self) -> VendorsFieldsAttach_field_to_vendorNamespace: ...
    @property
    def new_vendor_suggested_field(self) -> VendorsFieldsNew_vendor_suggested_fieldNamespace: ...
    @property
    def delete_vendor_field(self) -> VendorsFieldsDelete_vendor_fieldNamespace: ...

class VendorsFieldsDelete_vendor_fieldNamespace(LimbleEndpoint):
    pass

class VendorsFieldsNew_vendor_suggested_fieldNamespace(LimbleEndpoint):
    pass

class VendorsFieldsAttach_field_to_vendorNamespace(LimbleEndpoint):
    pass

class VendorsFieldsUpdate_vendor_field_valueNamespace(LimbleEndpoint):
    pass

class VendorsFieldsVendor_suggested_fieldsNamespace(LimbleEndpoint):
    pass

class VendorsFieldsVendor_fieldsNamespace(LimbleEndpoint):
    pass

class UsersNamespace(LimbleEndpoint):
    @property
    def roles(self) -> UsersRolesNamespace: ...
    @property
    def teams(self) -> UsersTeamsNamespace: ...
    @property
    def new_user(self) -> UsersNew_userNamespace: ...
    @property
    def update_user(self) -> UsersUpdate_userNamespace: ...
    @property
    def delete_user(self) -> UsersDelete_userNamespace: ...

class UsersDelete_userNamespace(LimbleEndpoint):
    pass

class UsersUpdate_userNamespace(LimbleEndpoint):
    pass

class UsersNew_userNamespace(LimbleEndpoint):
    pass

class UsersTeamsNamespace(object):
    @property
    def get_user_teams(self) -> UsersTeamsGet_user_teamsNamespace: ...
    @property
    def add_user_to_team(self) -> UsersTeamsAdd_user_to_teamNamespace: ...
    @property
    def remove_team_from_user(self) -> UsersTeamsRemove_team_from_userNamespace: ...

class UsersTeamsRemove_team_from_userNamespace(LimbleEndpoint):
    pass

class UsersTeamsAdd_user_to_teamNamespace(LimbleEndpoint):
    pass

class UsersTeamsGet_user_teamsNamespace(LimbleEndpoint):
    pass

class UsersRolesNamespace(object):
    @property
    def get_user_roles(self) -> UsersRolesGet_user_rolesNamespace: ...
    @property
    def add_user_to_role(self) -> UsersRolesAdd_user_to_roleNamespace: ...
    @property
    def remove_role_from_user(self) -> UsersRolesRemove_role_from_userNamespace: ...

class UsersRolesRemove_role_from_userNamespace(LimbleEndpoint):
    pass

class UsersRolesAdd_user_to_roleNamespace(LimbleEndpoint):
    pass

class UsersRolesGet_user_rolesNamespace(LimbleEndpoint):
    pass

class TasksNamespace(LimbleEndpoint):
    @property
    def invoices(self) -> TasksInvoicesNamespace: ...
    @property
    def instructions(self) -> TasksInstructionsNamespace: ...
    @property
    def images(self) -> TasksImagesNamespace: ...
    @property
    def labor(self) -> TasksLaborNamespace: ...
    @property
    def parts(self) -> TasksPartsNamespace: ...
    @property
    def comments(self) -> TasksCommentsNamespace: ...
    @property
    def tags(self) -> TasksTagsNamespace: ...
    @property
    def work_request_submissions(self) -> TasksWork_request_submissionsNamespace: ...
    @property
    def new_task(self) -> TasksNew_taskNamespace: ...
    @property
    def update_task(self) -> TasksUpdate_taskNamespace: ...
    @property
    def delete_task(self) -> TasksDelete_taskNamespace: ...

class TasksDelete_taskNamespace(LimbleEndpoint):
    pass

class TasksUpdate_taskNamespace(LimbleEndpoint):
    pass

class TasksNew_taskNamespace(LimbleEndpoint):
    pass

class TasksWork_request_submissionsNamespace(object):
    @property
    def list_wr_submissions(self) -> TasksWork_request_submissionsList_wr_submissionsNamespace: ...

class TasksWork_request_submissionsList_wr_submissionsNamespace(LimbleEndpoint):
    pass

class TasksTagsNamespace(LimbleEndpoint):
    @property
    def put_apply_task_tags(self) -> TasksTagsPut_apply_task_tagsNamespace: ...
    @property
    def delete_remove_task_tag(self) -> TasksTagsDelete_remove_task_tagNamespace: ...

class TasksTagsDelete_remove_task_tagNamespace(LimbleEndpoint):
    pass

class TasksTagsPut_apply_task_tagsNamespace(LimbleEndpoint):
    pass

class TasksCommentsNamespace(object):
    @property
    def task_comments(self) -> TasksCommentsTask_commentsNamespace: ...
    @property
    def add_task_comments(self) -> TasksCommentsAdd_task_commentsNamespace: ...

class TasksCommentsAdd_task_commentsNamespace(LimbleEndpoint):
    pass

class TasksCommentsTask_commentsNamespace(LimbleEndpoint):
    pass

class TasksPartsNamespace(object):
    @property
    def get_attached_parts(self) -> TasksPartsGet_attached_partsNamespace: ...
    @property
    def get_all_attached_parts(self) -> TasksPartsGet_all_attached_partsNamespace: ...
    @property
    def attach_part_to_task(self) -> TasksPartsAttach_part_to_taskNamespace: ...
    @property
    def delete_part_from_task(self) -> TasksPartsDelete_part_from_taskNamespace: ...

class TasksPartsDelete_part_from_taskNamespace(LimbleEndpoint):
    pass

class TasksPartsAttach_part_to_taskNamespace(LimbleEndpoint):
    pass

class TasksPartsGet_all_attached_partsNamespace(LimbleEndpoint):
    pass

class TasksPartsGet_attached_partsNamespace(LimbleEndpoint):
    pass

class TasksLaborNamespace(object):
    @property
    def task_labor(self) -> TasksLaborTask_laborNamespace: ...
    @property
    def get_labor_categories(self) -> TasksLaborGet_labor_categoriesNamespace: ...

class TasksLaborGet_labor_categoriesNamespace(LimbleEndpoint):
    pass

class TasksLaborTask_laborNamespace(LimbleEndpoint):
    pass

class TasksImagesNamespace(object):
    @property
    def task_instruction_image(self) -> TasksImagesTask_instruction_imageNamespace: ...
    @property
    def delete_task_instruction_image(self) -> TasksImagesDelete_task_instruction_imageNamespace: ...
    @property
    def upload_task_main_image(self) -> TasksImagesUpload_task_main_imageNamespace: ...
    @property
    def delete_task_main_image(self) -> TasksImagesDelete_task_main_imageNamespace: ...

class TasksImagesDelete_task_main_imageNamespace(LimbleEndpoint):
    pass

class TasksImagesUpload_task_main_imageNamespace(LimbleEndpoint):
    pass

class TasksImagesDelete_task_instruction_imageNamespace(LimbleEndpoint):
    pass

class TasksImagesTask_instruction_imageNamespace(LimbleEndpoint):
    pass

class TasksInstructionsNamespace(object):
    @property
    def options(self) -> TasksInstructionsOptionsNamespace: ...
    @property
    def task_instructions(self) -> TasksInstructionsTask_instructionsNamespace: ...
    @property
    def new_task_instruction(self) -> TasksInstructionsNew_task_instructionNamespace: ...
    @property
    def update_task_instruction(self) -> TasksInstructionsUpdate_task_instructionNamespace: ...
    @property
    def delete_task_instruction(self) -> TasksInstructionsDelete_task_instructionNamespace: ...
    @property
    def batch_task_instructions(self) -> TasksInstructionsBatch_task_instructionsNamespace: ...
    @property
    def get_task_instruction_by_id(self) -> TasksInstructionsGet_task_instruction_by_idNamespace: ...

class TasksInstructionsGet_task_instruction_by_idNamespace(LimbleEndpoint):
    pass

class TasksInstructionsBatch_task_instructionsNamespace(LimbleEndpoint):
    pass

class TasksInstructionsDelete_task_instructionNamespace(LimbleEndpoint):
    pass

class TasksInstructionsUpdate_task_instructionNamespace(LimbleEndpoint):
    pass

class TasksInstructionsNew_task_instructionNamespace(LimbleEndpoint):
    pass

class TasksInstructionsTask_instructionsNamespace(LimbleEndpoint):
    pass

class TasksInstructionsOptionsNamespace(object):
    @property
    def instruction_options(self) -> TasksInstructionsOptionsInstruction_optionsNamespace: ...
    @property
    def new_instruction_option(self) -> TasksInstructionsOptionsNew_instruction_optionNamespace: ...
    @property
    def delete_instruction_option(self) -> TasksInstructionsOptionsDelete_instruction_optionNamespace: ...
    @property
    def update_instruction_option(self) -> TasksInstructionsOptionsUpdate_instruction_optionNamespace: ...

class TasksInstructionsOptionsUpdate_instruction_optionNamespace(LimbleEndpoint):
    pass

class TasksInstructionsOptionsDelete_instruction_optionNamespace(LimbleEndpoint):
    pass

class TasksInstructionsOptionsNew_instruction_optionNamespace(LimbleEndpoint):
    pass

class TasksInstructionsOptionsInstruction_optionsNamespace(LimbleEndpoint):
    pass

class TasksInvoicesNamespace(LimbleEndpoint):
    @property
    def files(self) -> TasksInvoicesFilesNamespace: ...
    @property
    def attach_an_invoice_to_task(self) -> TasksInvoicesAttach_an_invoice_to_taskNamespace: ...
    @property
    def delete_invoice_from_task(self) -> TasksInvoicesDelete_invoice_from_taskNamespace: ...
    @property
    def update_an_invoice(self) -> TasksInvoicesUpdate_an_invoiceNamespace: ...

class TasksInvoicesUpdate_an_invoiceNamespace(LimbleEndpoint):
    pass

class TasksInvoicesDelete_invoice_from_taskNamespace(LimbleEndpoint):
    pass

class TasksInvoicesAttach_an_invoice_to_taskNamespace(LimbleEndpoint):
    pass

class TasksInvoicesFilesNamespace(object):
    @property
    def attach_a_file_to_an_invoice(self) -> TasksInvoicesFilesAttach_a_file_to_an_invoiceNamespace: ...
    @property
    def delete_file_from_invoice(self) -> TasksInvoicesFilesDelete_file_from_invoiceNamespace: ...

class TasksInvoicesFilesDelete_file_from_invoiceNamespace(LimbleEndpoint):
    pass

class TasksInvoicesFilesAttach_a_file_to_an_invoiceNamespace(LimbleEndpoint):
    pass

class PartsNamespace(LimbleEndpoint):
    @property
    def images(self) -> PartsImagesNamespace: ...
    @property
    def categories(self) -> PartsCategoriesNamespace: ...
    @property
    def fields(self) -> PartsFieldsNamespace: ...
    @property
    def logs(self) -> PartsLogsNamespace: ...
    @property
    def purchasables(self) -> PartsPurchasablesNamespace: ...
    @property
    def create_part(self) -> PartsCreate_partNamespace: ...
    @property
    def update_part(self) -> PartsUpdate_partNamespace: ...
    @property
    def delete_part(self) -> PartsDelete_partNamespace: ...
    @property
    def parts_usage(self) -> PartsParts_usageNamespace: ...

class PartsParts_usageNamespace(LimbleEndpoint):
    pass

class PartsDelete_partNamespace(LimbleEndpoint):
    pass

class PartsUpdate_partNamespace(LimbleEndpoint):
    pass

class PartsCreate_partNamespace(LimbleEndpoint):
    pass

class PartsPurchasablesNamespace(object):
    @property
    def get_purchasables(self) -> PartsPurchasablesGet_purchasablesNamespace: ...

class PartsPurchasablesGet_purchasablesNamespace(LimbleEndpoint):
    pass

class PartsLogsNamespace(object):
    @property
    def part_logs(self) -> PartsLogsPart_logsNamespace: ...
    @property
    def new_part_log(self) -> PartsLogsNew_part_logNamespace: ...
    @property
    def update_part_log(self) -> PartsLogsUpdate_part_logNamespace: ...
    @property
    def delete_part_log(self) -> PartsLogsDelete_part_logNamespace: ...
    @property
    def all_part_logs(self) -> PartsLogsAll_part_logsNamespace: ...

class PartsLogsAll_part_logsNamespace(LimbleEndpoint):
    pass

class PartsLogsDelete_part_logNamespace(LimbleEndpoint):
    pass

class PartsLogsUpdate_part_logNamespace(LimbleEndpoint):
    pass

class PartsLogsNew_part_logNamespace(LimbleEndpoint):
    pass

class PartsLogsPart_logsNamespace(LimbleEndpoint):
    pass

class PartsFieldsNamespace(object):
    @property
    def part_fields(self) -> PartsFieldsPart_fieldsNamespace: ...
    @property
    def part_suggested_fields(self) -> PartsFieldsPart_suggested_fieldsNamespace: ...
    @property
    def update_part_field_value(self) -> PartsFieldsUpdate_part_field_valueNamespace: ...
    @property
    def attach_field_to_part(self) -> PartsFieldsAttach_field_to_partNamespace: ...
    @property
    def new_part_suggested_field(self) -> PartsFieldsNew_part_suggested_fieldNamespace: ...
    @property
    def delete_part_field(self) -> PartsFieldsDelete_part_fieldNamespace: ...

class PartsFieldsDelete_part_fieldNamespace(LimbleEndpoint):
    pass

class PartsFieldsNew_part_suggested_fieldNamespace(LimbleEndpoint):
    pass

class PartsFieldsAttach_field_to_partNamespace(LimbleEndpoint):
    pass

class PartsFieldsUpdate_part_field_valueNamespace(LimbleEndpoint):
    pass

class PartsFieldsPart_suggested_fieldsNamespace(LimbleEndpoint):
    pass

class PartsFieldsPart_fieldsNamespace(LimbleEndpoint):
    pass

class PartsCategoriesNamespace(object):
    @property
    def create_part_category(self) -> PartsCategoriesCreate_part_categoryNamespace: ...
    @property
    def get_categories(self) -> PartsCategoriesGet_categoriesNamespace: ...
    @property
    def update_part_category(self) -> PartsCategoriesUpdate_part_categoryNamespace: ...
    @property
    def delete_part_category(self) -> PartsCategoriesDelete_part_categoryNamespace: ...

class PartsCategoriesDelete_part_categoryNamespace(LimbleEndpoint):
    pass

class PartsCategoriesUpdate_part_categoryNamespace(LimbleEndpoint):
    pass

class PartsCategoriesGet_categoriesNamespace(LimbleEndpoint):
    pass

class PartsCategoriesCreate_part_categoryNamespace(LimbleEndpoint):
    pass

class PartsImagesNamespace(object):
    @property
    def add_part_image(self) -> PartsImagesAdd_part_imageNamespace: ...
    @property
    def delete_part_image(self) -> PartsImagesDelete_part_imageNamespace: ...

class PartsImagesDelete_part_imageNamespace(LimbleEndpoint):
    pass

class PartsImagesAdd_part_imageNamespace(LimbleEndpoint):
    pass

class LocationsNamespace(LimbleEndpoint):
    @property
    def new_location(self) -> LocationsNew_locationNamespace: ...
    @property
    def update_location(self) -> LocationsUpdate_locationNamespace: ...
    @property
    def delete_location(self) -> LocationsDelete_locationNamespace: ...

class LocationsDelete_locationNamespace(LimbleEndpoint):
    pass

class LocationsUpdate_locationNamespace(LimbleEndpoint):
    pass

class LocationsNew_locationNamespace(LimbleEndpoint):
    pass

class AssetsNamespace(LimbleEndpoint):
    @property
    def image(self) -> AssetsImageNamespace: ...
    @property
    def fields(self) -> AssetsFieldsNamespace: ...
    @property
    def logs(self) -> AssetsLogsNamespace: ...
    @property
    def batch(self) -> AssetsBatchNamespace: ...
    @property
    def parts(self) -> AssetsPartsNamespace: ...
    @property
    def new_asset(self) -> AssetsNew_assetNamespace: ...
    @property
    def patch_asset(self) -> AssetsPatch_assetNamespace: ...
    @property
    def delete_asset(self) -> AssetsDelete_assetNamespace: ...
    @property
    def move_asset_to_another_location(self) -> AssetsMove_asset_to_another_locationNamespace: ...

class AssetsMove_asset_to_another_locationNamespace(LimbleEndpoint):
    pass

class AssetsDelete_assetNamespace(LimbleEndpoint):
    pass

class AssetsPatch_assetNamespace(LimbleEndpoint):
    pass

class AssetsNew_assetNamespace(LimbleEndpoint):
    pass

class AssetsPartsNamespace(object):
    @property
    def asset_parts(self) -> AssetsPartsAsset_partsNamespace: ...

class AssetsPartsAsset_partsNamespace(LimbleEndpoint):
    pass

class AssetsBatchNamespace(object):
    @property
    def batch_update_asset_fields(self) -> AssetsBatchBatch_update_asset_fieldsNamespace: ...

class AssetsBatchBatch_update_asset_fieldsNamespace(LimbleEndpoint):
    pass

class AssetsLogsNamespace(object):
    @property
    def files(self) -> AssetsLogsFilesNamespace: ...
    @property
    def asset_logs(self) -> AssetsLogsAsset_logsNamespace: ...
    @property
    def new_asset_log(self) -> AssetsLogsNew_asset_logNamespace: ...
    @property
    def update_asset_log(self) -> AssetsLogsUpdate_asset_logNamespace: ...
    @property
    def delete_asset_log(self) -> AssetsLogsDelete_asset_logNamespace: ...

class AssetsLogsDelete_asset_logNamespace(LimbleEndpoint):
    pass

class AssetsLogsUpdate_asset_logNamespace(LimbleEndpoint):
    pass

class AssetsLogsNew_asset_logNamespace(LimbleEndpoint):
    pass

class AssetsLogsAsset_logsNamespace(LimbleEndpoint):
    pass

class AssetsLogsFilesNamespace(object):
    @property
    def delete_asset_log_file(self) -> AssetsLogsFilesDelete_asset_log_fileNamespace: ...
    @property
    def add_asset_log_file(self) -> AssetsLogsFilesAdd_asset_log_fileNamespace: ...

class AssetsLogsFilesAdd_asset_log_fileNamespace(LimbleEndpoint):
    pass

class AssetsLogsFilesDelete_asset_log_fileNamespace(LimbleEndpoint):
    pass

class AssetsFieldsNamespace(object):
    @property
    def asset_fields(self) -> AssetsFieldsAsset_fieldsNamespace: ...
    @property
    def asset_suggested_fields(self) -> AssetsFieldsAsset_suggested_fieldsNamespace: ...
    @property
    def asset_field_history(self) -> AssetsFieldsAsset_field_historyNamespace: ...
    @property
    def new_asset_suggested_field(self) -> AssetsFieldsNew_asset_suggested_fieldNamespace: ...
    @property
    def update_asset_field_value(self) -> AssetsFieldsUpdate_asset_field_valueNamespace: ...
    @property
    def attach_field_to_asset(self) -> AssetsFieldsAttach_field_to_assetNamespace: ...
    @property
    def delete_asset_field(self) -> AssetsFieldsDelete_asset_fieldNamespace: ...

class AssetsFieldsDelete_asset_fieldNamespace(LimbleEndpoint):
    pass

class AssetsFieldsAttach_field_to_assetNamespace(LimbleEndpoint):
    pass

class AssetsFieldsUpdate_asset_field_valueNamespace(LimbleEndpoint):
    pass

class AssetsFieldsNew_asset_suggested_fieldNamespace(LimbleEndpoint):
    pass

class AssetsFieldsAsset_field_historyNamespace(LimbleEndpoint):
    pass

class AssetsFieldsAsset_suggested_fieldsNamespace(LimbleEndpoint):
    pass

class AssetsFieldsAsset_fieldsNamespace(LimbleEndpoint):
    pass

class AssetsImageNamespace(object):
    @property
    def add_asset_main_image(self) -> AssetsImageAdd_asset_main_imageNamespace: ...
    @property
    def delete_asset_main_image(self) -> AssetsImageDelete_asset_main_imageNamespace: ...

class AssetsImageDelete_asset_main_imageNamespace(LimbleEndpoint):
    pass

class AssetsImageAdd_asset_main_imageNamespace(LimbleEndpoint):
    pass

class MeNamespace(LimbleEndpoint):
    pass
