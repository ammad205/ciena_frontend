__author__ = 'awais'


from vnc_api import vnc_api
import configs


#####################################################################
############# Class for Service Chaining Functionality ##############
#####################################################################

class ServiceChaining():
    def __init__(self):
        self.vnc = vnc_api.VncApi(username=configs.username, password=configs.password, tenant_name=configs.tenant, api_server_host=configs.contrail_local_url)



    ## Required Params..
    # template : template type (firewall, NAT)
    # template_name : Name of the template from the front-end entered by user
    # fq_network : We may need this, passing the network from the front-end
    def launch_srv_instance(self, template, template_name, fq_newtork=None):
        project = self.vnc.project_read(fq_name = ['default-domain', 'demo'])

        instance = vnc_api.ServiceInstance(
                #name = 'service-dpi',
                name = template_name,
                parent_obj = project)

        properties = vnc_api.ServiceInstanceType(
                scale_out = vnc_api.ServiceScaleOutType())

        instance.set_service_instance_properties(properties)
        instance.set_service_template(template)

        self.vnc.service_instance_create(instance)

    ## Required Params.
    # template_name
    # service_mode
    # service_type
    # image_name
    def create_srv_template(self, template_name, service_mode, service_type, image_name=None):
        #template = vnc_api.ServiceTemplate(name = "service-dpi")
        template = vnc_api.ServiceTemplate(name = template_name)

        # properties = vnc_api.ServiceTemplateType(
        # service_mode = 'transparent',
        # service_type = 'firewall',
        # image_name = 'CentOS 6.4 Base')
        if image_name is None:
            properties = vnc_api.ServiceTemplateType(
              service_mode = service_mode,
              service_type = service_type,
              image_name = 'CentOS 6.4') #TODO: set a proper name that exists in openstack
        else:
            properties = vnc_api.ServiceTemplateType(
              service_mode = service_mode,
              service_type = service_type,
              image_name = image_name,
              )

        try:
            properties.add_interface_type(
            vnc_api.ServiceTemplateInterfaceType(
                service_interface_type = 'left', shared_ip = False))
            properties.add_interface_type(
            vnc_api.ServiceTemplateInterfaceType(
                service_interface_type = 'right', shared_ip = False))

            template.set_service_template_properties(properties)

            bc=self.vnc.service_template_create(template)
            print bc
            # call to service launch function

            fn = self.launch_srv_instance(template, template_name)


        except Exception,e:
            print e


    def network_poliy(self):
        pass

    def assoication_of_policy(self):
        pass

    def virtual_network(self, name, ip_pool=None, subnet_mask=None):
        vn_obj = vnc_api.VirtualNetwork(name) #'vn_name'
        vn_obj.add_network_ipam(vnc_api.NetworkIpam(),vnc_api.VnSubnetsType([vnc_api.IpamSubnetType(subnet = vnc_api.SubnetType(ip_pool, subnet_mask))]))
        virtual_network = self.vnc.virtual_network_create(vn_obj)
        print virtual_network
        return virtual_network