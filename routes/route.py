class Route:
    methods = []
    
    def route(self, request, *args):
        if request.method == 'GET':
            return self.GET(request, *args) 
        elif request.method == 'POST':
            return self.POST(request, *args)
        elif request.method == 'PUT':
            return self.PUT(request, *args)
        elif request.method == 'DELETE':
            return self.DELETE(request, *args)
