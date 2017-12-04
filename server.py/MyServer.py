import socket
import threading
import logging
import struct
from datetime import datetime
import psycopg2
from psycopg2.pool import PersistentConnectionPool
import socketserver

# 数据库连接池
pgsql_pool = PersistentConnectionPool(4, 10,
                                      dbname='monitor',
                                      user='yuvv',
                                      password='yuvv',
                                      host='localhost',
                                      port=5432)

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def setup(self):
        ip, port = self.client_address
        logging.info("%s:%d is connect!", ip, port)
        self.conn = pgsql_pool.getconn()
        self.conn.autocommit = True
        self.cur = self.conn.cursor()


    def handle(self):
        try:
            cur_thread = threading.current_thread()
            data = self.request.recv(56).strip()
            while data:
                logging.info('({0}) - {1}'.format(cur_thread.name, data.hex()))
                if data and len(data)==56:
                    # fnos为厂房编号和熔炉编号，indicator为后8位指示位
                    sno, fnos, a_i, b_i, c_i, i_default, a_v, b_v, c_v, e_speed, r_speed,\
                     a_action, b_action, c_action, indicators, dt = struct.unpack('!hBffffffffffffBf', data)
                    logging.info("data serial_no: %d received.", sno)
                    factory_no = fnos >> 6
                    furnace_no = fnos & 0x3F
                    status = (indicators & 0x80) > 0
                    feed = (indicators & 0x40) > 0
                    exhaust = (indicators & 0x20) > 0
                    d_time = datetime.fromtimestamp(dt)
                    self.cur.execute('INSERT INTO camera_data(factory_no, furnace_no, a_i, b_i, c_i, i_default,' +
                                    'a_v, b_v, c_v, e_speed, r_speed, a_action, b_action, c_action, status, feed, exhaust, d_time) values ' +
                                    '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                    (factory_no, furnace_no, a_i, b_i, c_i, i_default, a_v, b_v, c_v, e_speed, r_speed,
                                        a_action, b_action, c_action, status, feed, exhaust, d_time))

                    data = self.request.recv(56).strip()
        except psycopg2.Error as err:
            logging.error(str(err))
        except Exception as err:
            logging.error(str(err))


    def finish(self):
        ip, port = self.client_address
        logging.info("%s:%d is disconnect!", ip, port)
        self.cur.close()
        self.conn.commit()
        pgsql_pool.putconn(self.conn)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    logging.basicConfig(filename='_server.log', filemode='a',
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    HOST, PORT = "localhost", 54321

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

    server.serve_forever()
    logging.info("Server loop running...")
