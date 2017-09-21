class EmailConfiguration:
    def __init__(self, host, port, timeout, from_email, user, password):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.from_email = from_email
        self.user = user
        self.password = password


RASPBERRY_PI_BOT = EmailConfiguration('smtp-mail.outlook.com', 587, 10,
                                      'Raspberry Pi <raspberrypibot@outlook.com>',
                                      'raspberrypibot@outlook.com', '@Kuma929')
