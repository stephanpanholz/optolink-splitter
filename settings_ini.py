'''
   Copyright 2024 philippoo66
   
   Licensed under the GNU GENERAL PUBLIC LICENSE, Version 3 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       https://www.gnu.org/licenses/gpl-3.0.html

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

# serial ports +++++++++++++++++++
#port_vitoconnect = '/dev/ttyS0'  # '/dev/ttyS0'  older Pi:'/dev/ttyAMA0'  {optional} set None if no Vitoconnect
port_vitoconnect = None
port_optolink = '/dev/ttyVITO'   # '/dev/ttyUSB0'  {mandatory}

vs2timeout = 120                 # seconds to detect VS2 protocol on vitoconnect connection


# MQTT +++++++++++++++++++
mqtt = "192.168.77.120:1883"      # e.g. "192.168.0.123:1883"; set None to disable MQTT
mqtt_user = "mqtt:mqtt"     # "<user>:<pwd>"; set None for anonymous connect
mqtt_topic = "vito"              # "optolink"
mqtt_fstr = "{dpname}"           # "{dpaddr:04X}_{dpname}"
mqtt_listen = "vito/cmnd/#"        # "optolink/cmnd"; set None to disable listening
mqtt_respond = "vito/resp"       # "optolink/resp"


# TCP/IP +++++++++++++++++++
#tcpip_port = 65234         # e.g. 65234 is used by Viessdataby default; set None to disable TCP/IP
tcpip_port = None


# full raw timing
fullraw_eot_time = 0.05    # seconds. time no receive to decide end of telegram 
fullraw_timeout = 2        # seconds. timeout, return in any case 

# logging, info +++++++++++++++++++
log_vitoconnect = False    # logs communication with Vitoconnect (rx+tx telegrams)
show_opto_rx = True        # display on screen (no output when ran as service)

# format +++++++++++++++++++
max_decimals = 4
data_hex_format = '02x'    # set to '02X' for capitals
resp_addr_format = 'd'     # format of DP address in MQTT/TCPIP request response; e.g. 'd': decimal, '04X': hex 4 digits

# Viessdata utils +++++++++++++++++++
write_viessdata_csv = False
viessdata_csv_path = ""
buffer_to_write = 60
dec_separator = ","

# 1-wire sensors +++++++++++++++++++
w1sensors = {}
#     # addr : ('<w1_folder/sn>', '<slave_type>'),
#     0xFFF4 : ('28-3ce1d4438fd4', 'ds18b20'),   # highest known Optolink addr is 0xff17
#     0xFFFd : ('28-3ce1d443a4ed', 'ds18b20'),
# }


# polling datapoints +++++++++++++++++++
poll_interval = 0      # seconds. 0 for continuous, set -1 to disable Polling
poll_items = {
    # (Name, DpAddr, Len, Scale/Type, Signed)

    # Tabelle fuer Vitocalxxx-A mit Vitotronic 200 (Typ WO1B) (ab 04/2012)
    "betriebsart":(0xB000, 1, 1, False),			# betriebsart bit 4,5,6,7 comfort  bit 1 spar bit 0
    "kuehlbetrieb":(0x7100, 1, 1, False),
    "kuehlkreis":(0x7101, 1, 1, False),
    "freigabe_kuehlbetrieb":(0x71FE, 1, 1, False),
    "freigabe_heizstab_heizung":(0x7902, 1, 1, False),
    "freigabe_heizstab_warmwasser":(0x6015, 1, 1, False),
    "freigabe_warmwasser_einmalbereitung":(0xB020, 1, 1, False),
    "freigabe_heizstab":(0x7900, 1, 1, False),
    "freigabe_verdichter":(0x5000, 1, 1, False),
    "temperatur_raum_soll_normal":(0x2000, 2, 0.1, True),
    "temperatur_raum_soll_reduziert":(0x2001, 2, 0.1, True),
    "temperatur_raum_soll_party":(0x2002, 2, 0.1, True), # 2022???
    "heizkennlinie_niveau":(0x2006, 2, 0.1, True),
    "heizkennlinie_steigung":(0x2007, 2, 0.1, False),
    "hysterese_heizgrenze":(0x7003, 2, 0.1, False),
    "hysterese_kuehlgrenze":(0x7004, 2, 0.1, False),
    "hysterese_pufferspeicher":(0x7203, 2, 0.1, False),
    "hysterese_warmwasser":(0x6007, 2, 0.1, False),
    "hysterese_warmwasser_heizstab":(0x6008, 2, 0.1, False),
    "hysterese_warmwasser_heizstab_abschaltung":(0x601E, 2, 0.1, False),
    "temperatur_primaerkreis_min":(0x5016, 2, 0.1, True),
    "temperatur_primaerkreis_max":(0x5015, 2, 0.1, True),
    "temperatur_warmwasser_min":(0x6005, 2, 0.1, True),
    "temperatur_warmwasser_max":(0x6006, 2, 0.1, True),
    "temperatur_warmwasser_soll":(0x6000, 2, 0.1, True),
    "temperatur_warmwasser_soll2":(0x600C, 2, 0.1, True),
    "warmwasser_unterbrechung_max":(0x6012, 2, 1, False),
    "heizstab_leistung_max":(0x7907, 1, 1, False),
    "temperatur_heizstab_bivalenz":(0x790B, 2, 0.1, False),
    "temperatur_heizstab_vorlauf_max":(0x7904, 2, 0.1, False),
    "sekundaerpumpe_nachlaufzeit":(0x730B, 2, 1, False),
    "freigabe_waermeueberschussabnahme_heizkreis":(0x2011, 1, 1, False),
    "freigabe_waermeueberschussabnahme_warmwasserspeicher":(0x600F, 1, 1, False),
    "status_verdichter":(0x0400, 1, 1, False),
    "status_ventilator_stufe1":(0x0402, 1, 1, False),
    "status_ventilator_stufe2":(0x04B2, 1, 1, False),
    "status_heizstab_stufe1":(0x0408, 1, 1, False),
    "status_heizstab_stufe2":(0x0409, 1, 1, False),
    "status_sammelmeldung":(0x0411, 1, 1, False),
    "status_pumpe_heizkreis":(0x040D, 1, 1, False),
    "status_pumpe_warmwasserspeicher":(0x0496, 1, 1, False),
    "status_pumpe_pufferspeicher":(0x0484, 1, 1, False),
    "status_pumpe_zirkulation":(0x0490, 1, 1, False),
    "status_anforderung_kuehlen":(0x1903, 1, 1, False),
    "status_anforderung_heizen":(0x1904, 1, 1, False),
    "status_anforderung_warmwasser":(0x1905, 1, 1, False),
    "betriebsstunden_verdichter":(0x0580, 4, 2.7777778e-4, False), # 1/3600
    "betriebsstunden_verdichter_belastungsklasse1":(0x1620, 2, 1, False),
    "betriebsstunden_verdichter_belastungsklasse2":(0x1622, 2, 1, False),
    "betriebsstunden_verdichter_belastungsklasse3":(0x1624, 2, 1, False),
    "betriebsstunden_verdichter_belastungsklasse4":(0x1626, 2, 1, False),
    "betriebsstunden_verdichter_belastungsklasse5":(0x1628, 2, 1, False),
    "betriebsstunden_kaeltekreisumkehr":(0x059C, 4, 2.7777778e-4, False), # 1/3600
    "betriebsstunden_heizstab_stufe1":(0x0588, 4, 2.7777778e-4, False), # 1/3600
    "betriebsstunden_heizstab_stufe2":(0x0589, 4, 2.7777778e-4, False), # 1/3600
    "einschaltungen_verdichter":(0x0500, 4, 1, False),
    "einschaltungen_kaeltekreisumkehr":(0x051C, 4, 1, False),
    "einschaltungen_heizstab_stufe1":(0x0508, 4, 1, False),
    "einschaltungen_heizstab_stufe2":(0x0509, 4, 1, False),
    
    "temperatur_aussen":(0x0101, 2, 0.1, True),
    "temperatur_primaerkreis_vorlauf":(0x0103, 2, 0.1, True),
    "temperatur_primaerkreis_ruecklauf":(0x0104, 2, 0.1, True),
    "temperatur_sekundaerkreis_vorlauf":(0x0105, 2, 0.1, True),
    "temperatur_sekundaerkreis_ruecklauf":(0x0106, 2, 0.1, True),
    "temperatur_heizkreis_vorlauf":(0x010A, 2, 0.1, True),
    "temperatur_heizkreis_vorlauf_soll":(0x1800, 2, 0.1, True),
    "temperatur_pufferspeicher":(0x010B, 2, 0.1, True),
    "temperatur_warmwasserspeicher_oben":(0x010D, 2, 0.1, True),
    "temperatur_warmwasserspeicher_unten":(0x010E, 2, 0.1, True),
    "temperatur_fluessiggas":(0x0122, 2, 0.1, True),
    "temperatur_verdampfer":(0x0102, 2, 0.1, True),
    "temperatur_sauggas":(0x011E, 2, 0.1, True),
    "temperatur_heissgas":(0x0120, 2, 0.1, True),
    
    "druck_verdampfer":(0x0680, 2, 0.1, True),
    "druck_kondensator":(0x0682, 2, 0.1, True),
    
    "energiebilanz_jaz_total":(0x1680, 1, 0.1, False),
    "energiebilanz_jaz_heizen":(0x1681, 1, 0.1, False),
    "energiebilanz_jaz_warmwasser":(0x1682, 1, 0.1, False),
    "energiebilanz_warmwasser_strom":(0x16D0, 2, 0.1, False),
    "energiebilanz_warmwasser_waerme":(0x16D2, 2, 0.1, False),
    "energiebilanz_heizung_strom":(0x16D1, 2, 0.1, False),
    "energiebilanz_heizung_waerme":(0x16D3, 2, 0.1, False),

}

poll_items_keys = list(poll_items.keys())

