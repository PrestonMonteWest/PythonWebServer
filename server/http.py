class HttpResponse():
    def __init__(self, requestText):
        requestMessage = self.parseRequest(requestText)

        try:
            method, uri, version = requestMessage.split(' ')

            if version != 'HTTP/1.1':
                raise SomeError()

            if method == 'GET':
                # use uri to get object

            # parse body if post
            # generate complementary response dict
        except Exception:
            # generate server error response based on exceptions
            pass

    @staticmethod
    def parseRequest(requestText):
        '''
        Parse the request line, headers, and
        body into a dict for easier manipulation.
        '''

        requestLines = requestText.split('\n')
        message = {}

        message['request'] = requestLines.pop(0)
        for i, line in enumerate(requestLines):
            if line == '':
                break

            key, value = line.split(':')
            key = key.strip()
            value = value.strip()
            message[key] = value

        message['body'] = ''.join(requestLines[i+1:])
        return message

    def __str__(self):
        '''
        Generate string based on internal response message dict.
        '''

        # generate response message as string
        return ''
