import hashlib


class LazySigner(object):
    def sign(self, data):
        return hashlib.sha512((data + self.lazy_secret()).encode('utf-8')) \
            .hexdigest()

    def sign_request(self, request):
        shared_secret = "\0".join((
            request.path,
            request.body.decode(),
        ))
        return self.sign(shared_secret)

    def verify(self, data, signature):
        # TODO: Make this IND-CPA secure
        return self.sign(data) == signature

    def verify_request(self, request, signature):
        return self.sign_request(request) == signature
