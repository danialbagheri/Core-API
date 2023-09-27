from typing import Dict, Any

from common.services import TransactionalMailJetEmailService
from user.models import SentEmail


class SubscribeInvitationMailjetEmail(TransactionalMailJetEmailService):
    template_name = SentEmail.TEMPLATE_SUBSCRIBE_INVITATION
    template_config_key = 'subscribe-invitation-email-template-id'

    def _get_variables(self) -> Dict[str, Any]:
        return {}

    def _get_extra_data(self) -> str:
        return ''
