#!/bin/python3

class rsdp_pw_tmp():
    def __init__(self, sdp, ring, a_bsa, b_bsa, a_bsa_ipb, b_bsa_ipb, bin_port1, bin_port2):
        self.sdp_bsr01 = f'configure service sdp {sdp} mpls create \ndescription "TLDP-TO-BSA-{a_bsa}"\nfar-end {a_bsa_ipb}\nldp\nadv-mtu-override\nkeep-alive\nshutdown\nexit\nbinding\nport lag-{bin_port1}\nexit\nno shutdown\nexit all\n'
        self.sdp_bsr02 = f'configure service sdp {sdp} mpls create \ndescription "TLDP-TO-BSA-{b_bsa}"\nfar-end {b_bsa_ipb}\nldp\nadv-mtu-override\nkeep-alive\nshutdown\nexit\nbinding\nport lag-{bin_port2}\nexit\nno shutdown\nexit all\n'
        self.pw_bsr01 = f'configure pw-port {ring} create\ndescription "BSA-{a_bsa}_SDP-{sdp}_RING-{ring}"\nexit all\nconfigure redundancy multi-chassis peer 10.6.200.2 sync\nport pw-{ring} sync-tag "PW{ring}" create\nexit all\nconfigure service sdp {sdp} \nbinding\npw-port {ring} vc-id {ring} create\nvc-type vlan\nvlan-vc-tag {ring}\nno shutdown\nexit all\n'
        self.pw_bsr02 = f'configure pw-port {ring} create\ndescription "BSA-{b_bsa}_SDP-{sdp}_RING-{ring}"\nexit all\nconfigure redundancy multi-chassis peer 10.6.200.1 sync\nport pw-{ring} sync-tag "PW{ring}" create\nexit all\nconfigure service sdp {sdp} \nbinding\npw-port {ring} vc-id {ring} create\nvc-type vlan\nvlan-vc-tag {ring}\nno shutdown\nexit all\n'
        self.bsa_aa = f'system-view\nvsi {ring}\ndescription SUBSCRIBERS_BSR01-BSR02_RING-{ring}\npwsignal ldp\nvsi-id {ring}\npeer 10.6.200.1 upe\npeer 10.6.200.2 upe\nquit\nmtu 9168\nignore-ac-state\nquit\nquit\nsave\ny\n'
        self.bsa_a = f'system-view\nvsi {ring}\ndescription SUBSCRIBERS_BSR01-BSA{b_bsa}_RING-{ring}\npwsignal ldp\nvsi-id {ring}\npeer 10.6.200.1 upe\npeer {b_bsa_ipb} upe\nquit\nmtu 9168\nignore-ac-state\nquit\nquit\nsave\ny\n'
        self.bsa_b = f'system-view\nvsi {ring}\ndescription SUBSCRIBERS_BSR02-BSA{a_bsa}_RING-{ring}\npwsignal ldp\nvsi-id {ring}\npeer 10.6.200.2 upe\npeer {a_bsa_ipb} upe\nquit\nmtu 9168\nignore-ac-state\nquit\nquit\nsave\ny\n'

class sdp_tmp():
    def __init__(self, sdp, a_mku, b_mku, a_mku_ipb, b_mku_ipb, bin_port1, bin_port2):
        self.bsr01 = f'configure service sdp {sdp} mpls create \ndescription "TLDP-TO-MKU-{a_mku}"\nfar-end {a_mku_ipb}\nldp\nadv-mtu-override\nkeep-alive\nshutdown\nexit\nbinding\nport lag-{bin_port1}\nexit\nno shutdown\nexit all\n'
        self.bsr02 = f'configure service sdp {sdp} mpls create \ndescription "TLDP-TO-MKU-{b_mku}"\nfar-end {b_mku_ipb}\nldp\nadv-mtu-override\nkeep-alive\nshutdown\nexit\nbinding\nport lag-{bin_port2}\nexit\nno shutdown\nexit all\n'

class pw_tmp():
    def __init__(self, sdp, pw, a_mku, b_mku, a_mku_ipb, b_mku_ipb):
        self.bsr01 = f'configure pw-port {pw} create\ndescription "MKU-{a_mku}_SDP-{sdp}_RING-{pw}"\nexit all\nconfigure redundancy multi-chassis peer 10.6.200.2 sync\nport pw-{pw} sync-tag "PW{pw}" create\nexit all\nconfigure service sdp {sdp} \nbinding\npw-port {pw} vc-id {pw} create\nvc-type vlan\nvlan-vc-tag 4094\nno shutdown\nexit all\n'
        self.bsr02 = f'configure pw-port {pw} create\ndescription "MKU-{b_mku}_SDP-{sdp}_RING-{pw}"\nexit all\nconfigure redundancy multi-chassis peer 10.6.200.1 sync\nport pw-{pw} sync-tag "PW{pw}" create\nexit all\nconfigure service sdp {sdp} \nbinding\npw-port {pw} vc-id {pw} create\nvc-type vlan\nvlan-vc-tag 4094\nno shutdown\nexit all\n'
        self.mku_aa = f'system-view\nvsi {pw}\ndescription SUBSCRIBERS_BSR01-BSR02_RING-{pw}\npwsignal ldp\nvsi-id {pw}\npeer 10.6.200.1 upe\npeer 10.6.200.2 upe\nquit\nmtu 9168\nignore-ac-state\nquit\nquit\nsave\ny\n'
        self.mku_a = f'system-view\nvsi {pw}\ndescription SUBSCRIBERS_BSR01-MKU{b_mku}_RING-{pw}\npwsignal ldp\nvsi-id {pw}\npeer 10.6.200.1 upe\npeer {b_mku_ipb} upe\nquit\nmtu 9168\nignore-ac-state\nquit\nquit\nsave\ny\n'
        self.mku_b = f'system-view\nvsi {pw}\ndescription SUBSCRIBERS_BSR02-MKU{a_mku}_RING-{pw}\npwsignal ldp\nvsi-id {pw}\npeer 10.6.200.2 upe\npeer {a_mku_ipb} upe\nquit\nmtu 9168\nignore-ac-state\nquit\nquit\nsave\ny\n'

class operg_tmp():
    def __init__(self, sdp, ip_pool, a_mku, b_mku, a_mku_ipb, b_mku_ipb):
        self.bsr01 = f'configure service oper-group "SDP-{sdp}" create\nexit all\nconfigure service vprn 3\ninterface "SDP-{sdp}" create\ndescription "SDP-{sdp}"\naddress {ip_pool[-1]}/29\nvrrp 3\nbackup {ip_pool[0]}\npriority 250\noper-group "SDP-{sdp}"\nexit\nspoke-sdp {sdp}:{sdp} create\nno shutdown\nexit\nexit all\n'
        self.bsr02 = f'configure service oper-group "SDP-{sdp}" create\nexit all\nconfigure service vprn 3\ninterface "SDP-{sdp}" create\ndescription "SDP-{sdp}"\naddress {ip_pool[-2]}/29\nvrrp 3\nbackup {ip_pool[0]}\noper-group "SDP-{sdp}"\nexit\nspoke-sdp {sdp}:{sdp} create\nno shutdown\nexit\nexit all\n'
        self.mku_aa = f'system-view\nvsi {sdp}\ndescription OPER-GROUP_BSR01-BSR02_SDP-{sdp}\npwsignal ldp\nvsi-id {sdp}\npeer 10.6.200.1 upe\npeer 10.6.200.2 upe\nquit\nmtu 9168\nencapsulation ethernet\nignore-ac-state\nquit\nquit\nsave\ny\n'
        self.mku_a = f'system-view\nvsi {sdp}\ndescription OPER-GROUP_BSR01-MKU{b_mku}_SDP-{sdp}\npwsignal ldp\nvsi-id {sdp}\npeer 10.6.200.1 upe\npeer {b_mku_ipb} upe\nquit\nmtu 9168\nencapsulation ethernet\nignore-ac-state\nquit\nquit\nsave\ny\n'
        self.mku_b = f'system-view\nvsi {sdp}\ndescription OPER-GROUP_BSR02-MKU{a_mku}_SDP-{sdp}\npwsignal ldp\nvsi-id {sdp}\npeer 10.6.200.2 upe\npeer {a_mku_ipb} upe\nquit\nmtu 9168\nencapsulation ethernet\nignore-ac-state\nquit\nquit\nsave\ny\n'

class gi_tmp():
    def __init__(self, pw, srrp, mpsap):
        self.cctv_bsr01 = f'configure service vprn 100 subscriber-interface "CCTV"\ngroup-interface "CCTV-PW-{pw}" create\ndescription "CCTV FOR PW-{pw}"\narp-timeout 6000\nsrrp-enabled-routing\narp-populate\nhost-connectivity-verify interval 15 action remove retry-count 3\nipoe-session\nipoe-session-policy "IPSP-ERTH-STATIC"\nmin-auth-interval min 5 \nsap-session-limit 1000\nsession-limit 10000\nstateless-redundancy\nuser-db "LUDB-CCTV"\nno shutdown\nexit\ndata-trigger\nno shutdown\nexit\nremote-proxy-arp\nsap pw-{pw}:101 create\ndescription "PW-{pw}-CCTV"\ncpu-protection 100 mac-monitoring\ningress\nqos 1 shared-queuing\nexit\nsub-sla-mgmt\ndef-sub-profile "SP-CCTV"\ndef-sla-profile "SLA-CCTV-NAT"\nmulti-sub-sap 1000\nno shutdown\nexit\nexit\nsap pw-{pw}:{mpsap} create\nexit\nqos-route-lookup\nurpf-check\nexit\nsrrp {srrp} create\nmessage-path pw-{pw}:{mpsap}\npriority 250\nno shutdown\nexit\nexit all\n'
        self.cctv_bsr02 = f'configure service vprn 100 subscriber-interface "CCTV"\ngroup-interface "CCTV-PW-{pw}" create\ndescription "CCTV FOR PW-{pw}"\narp-timeout 6000\nsrrp-enabled-routing\narp-populate\nhost-connectivity-verify interval 15 action remove retry-count 3\nipoe-session\nipoe-session-policy "IPSP-ERTH-STATIC"\nmin-auth-interval min 5 \nsap-session-limit 1000\nsession-limit 10000\nstateless-redundancy\nuser-db "LUDB-CCTV"\nno shutdown\nexit\ndata-trigger\nno shutdown\nexit\nremote-proxy-arp\nsap pw-{pw}:101 create\ndescription "PW-{pw}-CCTV"\ncpu-protection 100 mac-monitoring\ningress\nqos 1 shared-queuing\nexit\nsub-sla-mgmt\ndef-sub-profile "SP-CCTV"\ndef-sla-profile "SLA-CCTV-NAT"\nmulti-sub-sap 1000\nno shutdown\nexit\nexit\nsap pw-{pw}:{mpsap} create\nexit\nqos-route-lookup\nurpf-check\nexit\nsrrp {srrp} create\nmessage-path pw-{pw}:{mpsap}\nno shutdown\nexit\nexit all\n'
        self.ipoe_bsr01 = f'configure service vprn 100 subscriber-interface "IPoE"\ngroup-interface "IPOE-PW-{pw}" create\ndescription "GROUP-INT FOR IPOE PW-{pw}"\narp-timeout 6000\nsrrp-enabled-routing\narp-populate\nhost-connectivity-verify interval 15 action remove retry-count 3\nipoe-session\nipoe-session-policy "IPSP-ERTH-STATIC"\nmin-auth-interval min 5 \nsap-session-limit 70\nsession-limit 10000\nstateless-redundancy\nuser-db "LUDB-DT"\nno shutdown\nexit\ndata-trigger\nno shutdown\nexit\nremote-proxy-arp\nsap pw-{pw}:{mpsap} create\nexit\nurpf-check\nexit\nsrrp {srrp} create\nmessage-path pw-{pw}:{mpsap}\npriority 250\nno shutdown\nexit\narp-host\nshutdown\nhost-limit 1024\nsap-host-limit 15\nexit all\n'
        self.ipoe_bsr02 = f'configure service vprn 100 subscriber-interface "IPoE"\ngroup-interface "IPOE-PW-{pw}" create\ndescription "GROUP-INT FOR IPOE PW-{pw}"\narp-timeout 6000\nsrrp-enabled-routing\narp-populate\nhost-connectivity-verify interval 15 action remove retry-count 3\nipoe-session\nipoe-session-policy "IPSP-ERTH-STATIC"\nmin-auth-interval min 5 \nsap-session-limit 70\nsession-limit 10000\nstateless-redundancy\nuser-db "LUDB-DT"\nno shutdown\nexit\ndata-trigger\nno shutdown\nexit\nremote-proxy-arp\nsap pw-{pw}:{mpsap} create\nexit\nurpf-check\nexit\nsrrp {srrp} create\nmessage-path pw-{pw}:{mpsap}\nno shutdown\nexit\narp-host\nshutdown\nhost-limit 1024\nsap-host-limit 15\nexit all\n'
        self.sdef_bsr01 = f'configure service vprn 100 subscriber-interface "SUB-DEFAULT"\ngroup-interface "DEFAULT-PW-{pw}" create\ndescription "DEFAULT-PW-{pw}"\nipv6\nrouter-advertisements\nother-stateful-configuration\nprefix-options\nautonomous\nexit\nno shutdown\nexit\ndhcp6\nproxy-server\nclient-applications ppp\nno shutdown\nexit\nrelay\nsource-address 2a02:2698:9800::503\nlink-address 2a02:2698:9800::503\nserver 2a02:2698:9800::503\nclient-applications ppp\nno shutdown\nexit\nexit\nexit\nsrrp-enabled-routing\narp-populate\ndhcp\npython-policy "PY-DHCP-OPT82"\nproxy-server\nemulated-server 176.215.186.254\nlease-time min 30 \nno shutdown\nexit\noption\naction keep\ncircuit-id\nremote-id\nvendor-specific-option\npool-name\nexit\nexit\nserver 176.213.132.70 \ntrusted\nlease-populate 200\nclient-applications dhcp ppp\ngi-address 176.215.186.254\nuser-db "LUDB-DHCP-M"\nno shutdown\nexit\nshcv-policy "DHCP-SHCV"\nredundant-interface "RED-12"\nremote-proxy-arp\nsap pw-{pw}:{mpsap} create\nexit\nurpf-check\nexit\nsrrp {srrp} create\nmessage-path pw-{pw}:{mpsap}\npriority 200\nsend-fib-population-packets outer-tag-only\none-garp-per-sap\nno shutdown\nexit\npppoe\npolicy "PPPOE-POLICY-DELAY3"\nsession-limit 32000\nsap-session-limit 4000\nuser-db "LUDB-PPPOE"\nno shutdown\nexit all\nconfigure service vpls 1\nsap pw-{pw}:* capture-sap create\ncpu-protection 100 mac-monitoring\ntrigger-packet dhcp pppoe\ndhcp-python-policy "PY-DHCP-OPT82"\ndhcp-user-db "LUDB-DHCP-M"\npppoe-policy "PPPOE-POLICY-DELAY3"\npppoe-user-db "LUDB-PPPOE"\ntrack-srrp {srrp}\nmsap-defaults\ngroup-interface "DEFAULT-PW-{pw}"\npolicy "PL-MSAP-DEFAULT"\nservice 100\nexit\nhost-lockout-policy "LOCK-BAD-AUTH"\nno shutdown\nexit all\n'
        self.sdef_bsr02 = f'configure service vprn 100 subscriber-interface "SUB-DEFAULT"\ngroup-interface "DEFAULT-PW-{pw}" create\ndescription "DEFAULT-PW-{pw}"\nipv6\nrouter-advertisements\nother-stateful-configuration\nprefix-options\nautonomous\nexit\nno shutdown\nexit\ndhcp6\nproxy-server\nclient-applications ppp\nno shutdown\nexit\nrelay\nsource-address 2a02:2698:9800::503\nlink-address 2a02:2698:9800::503\nserver 2a02:2698:9800::503\nclient-applications ppp\nno shutdown\nexit\nexit\nexit\nsrrp-enabled-routing\narp-populate\ndhcp\npython-policy "PY-DHCP-OPT82"\nproxy-server\nemulated-server 176.215.186.254\nlease-time min 30 \nno shutdown\nexit\noption\naction keep\ncircuit-id\nremote-id\nvendor-specific-option\npool-name\nexit\nexit\nserver 176.213.132.70 \ntrusted\nlease-populate 200\nclient-applications dhcp ppp\ngi-address 176.215.186.254\nuser-db "LUDB-DHCP-M"\nno shutdown\nexit\nshcv-policy "DHCP-SHCV"\nredundant-interface "RED-21"\nremote-proxy-arp\nsap pw-{pw}:{mpsap} create\nexit\nurpf-check\nexit\nsrrp {srrp} create\nmessage-path pw-{pw}:{mpsap}\npriority 150\nsend-fib-population-packets outer-tag-only\none-garp-per-sap\nno shutdown\nexit\npppoe\npolicy "PPPOE-POLICY-DELAY3"\nsession-limit 32000\nsap-session-limit 4000\nuser-db "LUDB-PPPOE"\nno shutdown\nexit all\nconfigure service vpls 1\nsap pw-{pw}:* capture-sap create\ncpu-protection 100 mac-monitoring\ntrigger-packet dhcp pppoe\ndhcp-python-policy "PY-DHCP-OPT82"\ndhcp-user-db "LUDB-DHCP-M"\npppoe-policy "PPPOE-POLICY-DELAY3"\npppoe-user-db "LUDB-PPPOE"\ntrack-srrp {srrp}\nmsap-defaults\ngroup-interface "DEFAULT-PW-{pw}"\npolicy "PL-MSAP-DEFAULT"\nservice 100\nexit\nhost-lockout-policy "LOCK-BAD-AUTH"\nno shutdown\nexit all\n'
        self.aenf_bsr01 = f'configure service vprn 140 subscriber-interface "ACCESS-ENFORTA" \ngroup-interface "ENFORTA-PW-{pw}" create\ndescription "ENFORTA-PW-{pw}"\nsrrp-enabled-routing\narp-populate\nhost-connectivity-verify interval 15 action remove retry-count 3\nipoe-session\nipoe-session-policy "IPSP-ERTH-STATIC"\nsap-session-limit 10\nsession-limit 32000\nstateless-redundancy\nuser-db "LUDB-ENFORTA"\nno shutdown\nexit\ndata-trigger\nno shutdown\nexit\noper-up-while-empty\nremote-proxy-arp\nsap pw-{pw}:{mpsap} create\ndescription "FOR-SRRP-{srrp}"\nexit\nsap pw-{pw}:103 create\ndescription "VOIP"\ncpu-protection 100 mac-monitoring\ningress\nqos 1 shared-queuing\nexit\nanti-spoof nh-mac\nsub-sla-mgmt\ndef-sub-id use-sap-id\ndef-sub-profile "SP-ENFORTA"\ndef-sla-profile "SLA-REDIRECT"\nmulti-sub-sap 10\nno shutdown\nexit\nexit\nurpf-check\nexit\nsrrp {srrp} create\nmessage-path pw-{pw}:{mpsap}\npriority 250\nno shutdown\nexit\narp-host\nshutdown\nhost-limit 1024\nsap-host-limit 15\nexit all\n'
        self.aenf_bsr02 = f'configure service vprn 140 subscriber-interface "ACCESS-ENFORTA" \ngroup-interface "ENFORTA-PW-{pw}" create\ndescription "ENFORTA-PW-{pw}"\nsrrp-enabled-routing\narp-populate\nhost-connectivity-verify interval 15 action remove retry-count 3\nipoe-session\nipoe-session-policy "IPSP-ERTH-STATIC"\nsap-session-limit 10\nsession-limit 32000\nstateless-redundancy\nuser-db "LUDB-ENFORTA"\nno shutdown\nexit\ndata-trigger\nno shutdown\nexit\noper-up-while-empty\nremote-proxy-arp\nsap pw-{pw}:{mpsap} create\ndescription "FOR-SRRP-{srrp}"\nexit\nsap pw-{pw}:103 create\ndescription "VOIP"\ncpu-protection 100 mac-monitoring\ningress\nqos 1 shared-queuing\nexit\nanti-spoof nh-mac\nsub-sla-mgmt\ndef-sub-id use-sap-id\ndef-sub-profile "SP-ENFORTA"\ndef-sla-profile "SLA-REDIRECT"\nmulti-sub-sap 10\nno shutdown\nexit\nexit\nurpf-check\nexit\nsrrp {srrp} create\nmessage-path pw-{pw}:{mpsap}\nno shutdown\nexit\narp-host\nshutdown\nhost-limit 1024\nsap-host-limit 15\nexit all\n'

class vpls_tmp():
    def __init__(self, new_vpls, mtu):
        self.bs_bsr01 = f'configure service vpls {new_vpls} create customer 1\ndescription "CREATED_BY_SCRIPT"\nservice-mtu {mtu}\nmesh-sdp 12:{new_vpls} create\nno shutdown\nexit\nno shutdown\nexit\n'
        self.bs_bsr02 = f'configure service vpls {new_vpls} create customer 1\ndescription "CREATED_BY_SCRIPT"\nservice-mtu {mtu}\nmesh-sdp 21:{new_vpls} create\nno shutdown\nexit\nno shutdown\nexit\n'
        self.rt_bsr01 = f'configure service vpls {new_vpls} create customer 1\ndescription "CREATED_BY_SCRIPT"\nservice-mtu {mtu}\nsplit-horizon-group "SDP" create\nexit\nbgp\nroute-distinguisher 2002:{new_vpls}\nroute-target export target:9049:{new_vpls} import target:9049:{new_vpls}\npw-template-binding 1 split-horizon-group "SDP"\nmonitor-oper-group "VRRP-3"\nexit\nexit\nbgp-vpls\nmax-ve-id 128\nve-name "bsr"\nve-id 1\nexit\nno shutdown\nexit\nmesh-sdp 12:{new_vpls} create\nno shutdown\nexit\nno shutdown\nexit\n'
        self.rt_bsr02 = f'configure service vpls {new_vpls} create customer 1\ndescription "CREATED_BY_SCRIPT"\nservice-mtu {mtu}\nsplit-horizon-group "SDP" create\nexit\nbgp\nroute-distinguisher 2002:{new_vpls}\nroute-target export target:9049:{new_vpls} import target:9049:{new_vpls}\npw-template-binding 1 split-horizon-group "SDP"\nmonitor-oper-group "VRRP-3"\nexit\nexit\nbgp-vpls\nmax-ve-id 128\nve-name "bsr"\nve-id 1\nexit\nno shutdown\nexit\nmesh-sdp 21:{new_vpls} create\nno shutdown\nexit\nno shutdown\nexit\n'

class sap_tmp():
    def __init__(self, mode, *args):
        if mode == 3: #remove SAP from VPLS
            vpls, sap = args
            self.vpls_del = f'configure service vpls {vpls}\nsap {sap} shutdown\nno sap {sap}\n'
        if mode == 1: #add SAP to VPLS
            vpls, sap, rate = args
            self.vpls_add = f'configure service vpls {vpls}\nsap {sap} create\ndescription "ADDED_BY_SCRIPT"\ningress\nqos 55 multipoint-shared\nqueue-override\nqueue 1 create\nrate {rate} cir {rate}\nexit\nexit\nexit\negress\nqos 55\nqueue-override\nqueue 1 create\nrate {rate} cir {rate}\nexit\nexit\nexit\nno shutdown\nexit\nexit all\n'
        if mode == 0: #add SAP and interface to VPRN
            vprn, ifc, opg, ip, sap, cmbs, rate = args
            self.vprn_add = f'configure service vprn {vprn} interface {ifc} create\ndescription "ADDED_BY_SCRIPT"\nmonitor-oper-group "{opg}"\naddress {ip}\nmac 00:00:5e:00:02:ff\nip-mtu 1500\nsap {sap} create\ningress\nqos 55\nqueue-override\nqueue 1 create\ncbs {cmbs}\nmbs {cmbs} kilobytes\nrate {rate} cir {rate}\nexit\nexit\nexit\negress\nqos 55\nqueue-override\nqueue 1 create\ncbs {cmbs}\nmbs {cmbs} kilobytes\nrate {rate} cir {rate}\nexit\nexit\nexit\nexit\nexit all\n'
        if mode == 2: #remove SAP and interface from VPRN
            vprn, ifc, sap = args
            self.vprn_del = f'configure service vprn {vprn}\ninterface "{ifc}"\nsap {sap} shutdown\nno sap {sap}\nshutdown\nexit\nno interface "{ifc}"\nexit all\n'