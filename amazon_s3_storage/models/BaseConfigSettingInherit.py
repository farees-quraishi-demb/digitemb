import ast
from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval
import logging
_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def _default_s3_config(self):
        res = self.env['s3.config'].sudo().search([], limit=1)
        return res.id

    def open_s3_conf(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Amazon S3 Configuration',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 's3.config',
            'res_id': self.s3_config_id.id,
            'target': 'current',
        }

    s3_config_id = fields.Many2one('s3.config', string="S3 Config",
                                   default=_default_s3_config, ondelete='cascade')


    def s3_get_values(self):
        s3_config_id = self.env['s3.config'].sudo().search([],limit=1)
        res ={}
        res.update(
            amazonS3bucket_name=s3_config_id.amazonS3bucket_name,
            amazonS3secretkey=s3_config_id.amazonS3secretkey,
            amazonS3accessKeyId= s3_config_id.amazonS3accessKeyId,
            storage_type = s3_config_id.storage_type,
            region_name = s3_config_id.region_name,
            s3_sync_domain = s3_config_id.s3_sync_domain and safe_eval(s3_config_id.s3_sync_domain) or [],
            expireIn = _getExpireValue(attr=s3_config_id.image_expire,value = s3_config_id.image_expire_val ),
            image_expire = s3_config_id.image_expire,
            image_expire_val = s3_config_id.image_expire_val,
        )
        return res
