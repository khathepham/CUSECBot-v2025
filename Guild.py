class Guild:
    guild_id = None
    verification_channel = None
    logs_channel = None

    def __init__(self, guild_id, verification_channel=None, logs_channel=None, delegate_role=None, sponsor_role=None,
                 speaker_role=None, panelist_role=None, vip_role=None, verification_requests_channel=None, moderation_role=None):
        self.guild_id = guild_id
        self.verification_channel = verification_channel
        self.logs_channel = logs_channel
        self.delegate_role = delegate_role
        self.vip_role = vip_role
        self.sponsor_role = sponsor_role
        self.speaker_role = speaker_role
        self.panelist_role = panelist_role
        self.verification_requests_channel = verification_requests_channel
        self.moderation_role = moderation_role

    def to_json(self):
        return {
            "_id": self.guild_id,
            "guild_id": self.guild_id,
            "verification_channel": self.verification_channel,
            "logs_channel": self.logs_channel,
            "delegate_role": self.delegate_role,
            "vip_role": self.vip_role,
            "sponsor_role": self.sponsor_role,
            "speaker_role": self.speaker_role,
            "panelist_role": self.panelist_role,
            "verification_requests_channel": self.verification_requests_channel,
            "moderation_role": self.moderation_role
        }

    @classmethod
    def from_json(cls, guild_obj: dict):
        return Guild(
            guild_id=guild_obj.get("_id"),
            verification_channel=guild_obj.get("verification_channel"),
            logs_channel=guild_obj.get("logs_channel"),
            delegate_role=guild_obj.get("delegate_role"),
            vip_role=guild_obj.get("vip_role"),
            sponsor_role=guild_obj.get("sponsor_role"),
            speaker_role=guild_obj.get("speaker_role"),
            panelist_role=guild_obj.get("panelist_role"),
            verification_requests_channel=guild_obj.get("verification_requests_channel"),
            moderation_role=guild_obj.get("moderation_role")
        )
