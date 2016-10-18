#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.mail import EmailMultiAlternatives
from django.core.mail.utils import DNS_NAME
from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings
import smtplib
import ssl
from ..logger import SysLogger


def mail_to_one(subject, content, recipient, sender=settings.EMAIL_HOST_USER, headers={"From": "高德软件 <no-reply@amap.com>", "Reply-To": "no-reply@amap.com"}):
    '''基于Django给一位收件人发邮件，用于线上需要指定header的邮件发送'''
    #'@autonavi-testing-2015.com'域名用于自动化测试，不发验证码
    if recipient.endswith('@autonavi-testing-2015.com'):
        return True
    try:
        msg = EmailMultiAlternatives(subject, content, sender, [recipient], headers=headers)
        msg.attach_alternative(content, "text/plain")
        return msg.send()
    except Exception as ex:
        SysLogger.exception(ex)
        return 0


def mail_to_list(mail_list=[], subject='', content='', files=[], is_log=False):
    '''基于smtplib给一个/一批人发送邮件，用于不需要设置headers的邮件发送。支持带附件。

    @subject -- 主题，unicode
    @content -- 内容，unicode
    @files -- 附件路径
    @is_log -- 是否记日志
    '''
    try:
        if is_log:
            SysLogger.info(content)
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = ';'.join(mail_list)
        msg["Accept-Language"] = "zh-CN"
        msg["Accept-Charset"] = "ISO-8859-1,utf-8"
        msg.attach(MIMEText(content, _charset='utf-8'))
        for f in files:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(f, "rb").read())
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
            msg.attach(part)

        if settings.EMAIL_USE_SSL:
            smtp = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=settings.EMAIL_TIMEOUT)
        else:
            smtp = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=settings.EMAIL_TIMEOUT)
        if settings.EMAIL_USE_TLS:
            smtp.starttls()
        # 兼容白名单不需要login的情况
        try:
            smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        except:
            pass
        smtp.sendmail(settings.EMAIL_HOST_USER, mail_list, msg.as_string())
        smtp.quit()
    except Exception as e:
        SysLogger.exception(e)


class SSLEmailBackend(EmailBackend):
    '''支持ssl邮件发送的EmailBackend'''

    def open(self):
        """
        Ensures we have a connection to the email server. Returns whether or
        not a new connection was required (True or False).
        """
        if self.connection:
            # Nothing to do if the connection is already open.
            return False

        self.use_ssl = getattr(settings, 'EMAIL_USE_SSL', False)
        connection_class = smtplib.SMTP_SSL if self.use_ssl else smtplib.SMTP
        # If local_hostname is not specified, socket.getfqdn() gets used.
        # For performance, we use the cached FQDN for local_hostname.
        connection_params = {'local_hostname': DNS_NAME.get_fqdn()}
        try:
            self.connection = connection_class(self.host, self.port, **connection_params)

            # TLS/SSL are mutually exclusive, so only attempt TLS over
            # non-secure connections.
            if not self.use_ssl and self.use_tls:
                self.connection.ehlo()
                self.connection.starttls()
                self.connection.ehlo()
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except smtplib.SMTPException:
            if not self.fail_silently:
                raise

    def close(self):
        """Closes the connection to the email server."""
        if self.connection is None:
            return
        try:
            try:
                self.connection.quit()
            except (ssl.SSLError, smtplib.SMTPServerDisconnected):
                # This happens when calling quit() on a TLS connection
                # sometimes, or when the connection was already disconnected
                # by the server.
                self.connection.close()
            except smtplib.SMTPException:
                if self.fail_silently:
                    return
                raise
        finally:
            self.connection = None
