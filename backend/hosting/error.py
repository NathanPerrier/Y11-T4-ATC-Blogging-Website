from backend.config import *

def register_error_handlers(error):
    @error.errorhandler(404)
    def page_not_found(e, error=404):
        return render_template('error.html', title="Page Not Found", error=error, desc='We’re sorry, the page you have looked for does not exist in our website! Maybe go back to our home page or user the navigation bar?', user=current_user), error

    @error.errorhandler(405)
    def method_not_allowed(e, error=405):
         return render_template('error.html', title="Method Not Allowed", error=error, desc='The requested method is not allowed. Please refer to the allowed methods and try again or return home.', user=current_user), error
     
    @error.errorhandler(400)
    def bad_request(e, error=400):
        return render_template('error.html', title="Bad Request", error=error, desc='There was an issue processing your request. This could be due to an imvalid action or input. Please try again or return home.', user=current_user), error

    @error.errorhandler(401)
    def unauthorized(e, error=401):
        return render_template('error.html', title="Unauthorized", error=error, desc="You are not authorized to access this page. Please log in with the correct credentials and try again or return home.", user=current_user), error

    @error.errorhandler(403)
    def forbidden(e, error=403):
        return render_template('error.html', title="Forbidden", error=error, desc="You do not have access rights to the content. Please check your permissions and try again or return home.", user=current_user), error
    
    @error.errorhandler(406)
    def not_acceptable(e, error=406):
        return render_template('error.html', title="Not Acceptable", error=error, desc="The server cannot produce a response matching the list of acceptable values defined in the request's headers. Please check your request and try again or return home.", user=current_user), error

    @error.errorhandler(408)
    def request_timeout(e, error=408):
        return render_template('error.html', title="Request Timeout", error=error, desc="Your request took too long to load. his is most commonly caused by a delay in the client's response. Please try again or return home.", user=current_user), error

    @error.errorhandler(410)
    def resource_gone(e, error=410):
        return render_template('error.html', title="Resource Gone", error=error, desc="The resource you are looking for is no longer available. Please try again or return home.", user=current_user), error

    @error.errorhandler(500)
    def internal_sever_error(e, error=500):
        return render_template('error.html', title="Internal Server Error", error=error, desc="There is an error in loading the sever. Plase try again later.", user=current_user), error

    @error.errorhandler(502)
    def bad_gateway(e, error=502):
        return render_template('error.html', title="Bad Gateway", error=error, desc="The server received an invalid response from the upstream server while trying to fulfill the request. Please try again or return home.", user=current_user), error
    
    @error.errorhandler(503)
    def service_unavailable(e, error=503):
        return render_template('error.html', title="Service Unavailable", error=error, desc="The server is currently unable to handle the request due to a temporary overload or scheduled maintenance. Please try again later.", user=current_user), error
    
    @error.errorhandler(504)
    def gateway_timeout(e, error=504):
        return render_template('error.html', title="Gateway Timeout", error=error, desc="The server did not receive a timely response from the upstream server while trying to fulfill the request. Please try again or return home.", user=current_user), error
    
    @error.errorhandler(505)
    def http_version_not_supported(e, error=505):
        return render_template('error.html', title="HTTP Version Not Supported", error=error, desc="The server does not support the HTTP protocol version used in the request. Please try again or return home.", user=current_user), error
    
    # @error.errorhandler(511)
    # def network_authentication_required(e, error=511):
    #     return render_template('error.html', title="Network Authentication Required", error=error, desc="The client needs to authenticate to gain network access. Please try again or return home.", user=current_user), error
    
    # @error.errorhandler(520)
    # def unknown_error(e, error=520):
    #     return render_template('error.html', title="Unknown Error", error=error, desc="The server has encountered an unknown error. Please try again or return home.", user=current_user), error
    
    # @error.errorhandler(522)
    # def connection_timed_out(e, error=522):
    #     return render_template('error.html', title="Connection Timed Out", error=error, desc="The server connection timed out. Please try again or return home.", user=current_user), error
    
    # @error.errorhandler(524)
    # def a_timeout_occurred(e, error=524):
    #     return render_template('error.html', title="A Timeout Occurred", error=error, desc="A timeout occurred. Please try again or return home.", user=current_user), error
    
    # @error.errorhandler(525)
    # def ssl_handshake_failed(e, error=525):
    #     return render_template('error.html', title="SSL Handshake Failed", error=error, desc="The SSL handshake failed. Please try again or return home.", user=current_user), error
    
    # @error.errorhandler(526)
    # def invalid_ssl_certificate(e, error=526):
    #     return render_template('error.html', title="Invalid SSL Certificate", error=error, desc="The server could not validate the SSL certificate. Please try again or return home.", user=current_user), error
    
    # @error.errorhandler(527)
    # def railgun_error(e, error=527):
    #     return render_template('error.html', title="Railgun Error", error=error, desc="The request timed out or failed after the WAN connection had been established. Please try again or return home.", user=current_user), error
    
    # @error.errorhandler(530)
    # def origin_dns_error(e, error=530):
    #     return render_template('error.html', title="Origin DNS Error", error=error, desc="The server could not resolve your request for unknown reasons. Please try again or return home.", user=current_user), error
    
    # @error.errorhandler(598)
    # def network_read_timeout_error(e, error=598):
    #     return render_template('error.html', title="Network Read Timeout Error", error=error, desc="The network read timed out. Please try again or return home.", user=current_user), error
    
    # @error.errorhandler(599)
    # def network_connect_timeout_error(e, error=599):
    #     return render_template('error.html', title="Network Connect Timeout Error", error=error, desc="The network connection timed out. Please try again or return home.", user=current_user), error
    
