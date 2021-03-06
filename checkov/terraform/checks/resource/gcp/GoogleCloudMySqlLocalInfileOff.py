from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck


class GoogleCloudMySqlLocalInfileOff(BaseResourceCheck):
    def __init__(self):
        name = "Ensure MySQL database 'local_infile' flag is set to 'off'"
        check_id = "CKV_GCP_50"
        supported_resources = ['google_sql_database_instance']
        categories = [CheckCategories.GENERAL_SECURITY]
        super().__init__(name=name, id=check_id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        """
            Looks for google_sql_database_instance which enables local_infile:
            :param
            conf: google_sql_database_instance
            configuration
            :return: < CheckResult >
        """
        if 'database_version' in conf.keys():
            key = conf['database_version'][0]
            if 'MYSQL' in key:
                if 'settings' in conf.keys():
                    for attribute in conf['settings'][0]:
                        if attribute == 'database_flags':
                            for flag in conf['settings'][0]['database_flags']:
                                if (flag['name'][0] == 'local_infile') and (flag['value'][0] == 'on'):
                                    return CheckResult.FAILED
        return CheckResult.PASSED


check = GoogleCloudMySqlLocalInfileOff()
