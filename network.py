"""
Mô đun quản lý kết nối mạng (Networking).
Cung cấp kiến trúc liên lạc ngang hàng (Peer-to-Peer) qua giao thức TCP Socket
để đồng bộ hóa trạng thái ứng dụng cho chế độ chơi nhiều người (Online Multiplayer).
"""
import socket
import threading
import pickle

class GameNetwork:
    """
    Lớp bọc (Wrapper) xử lý toàn bộ các tác vụ liên quan đến Socket, 
    tuần tự hóa dữ liệu (Serialization) bằng Pickle, và quản lý luồng dữ liệu 
    nhận/gửi một cách bất đồng bộ để không chặn (blocking) vòng lặp Pygame.
    """
    def __init__(self):
        """
        Khởi tạo các thành phần giao tiếp mạng tiêu chuẩn: Socket client, 
        biến định danh vai trò (Host/Client), danh sách hàng đợi bản tin, và cơ chế Khóa luồng (Lock).
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = None
        self.is_host = False
        self.connected = False
        self.received_data = []
        self.lock = threading.Lock()

    def host_game(self, port=5555):
        """
        Thiết lập vai trò Máy chủ (Host). Binding địa chỉ và lắng nghe các yêu cầu kết nối
        trên cổng (port) xác định thông qua một luồng chạy nền (Daemon thread).
        """
        self.is_host = True
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0', port))
        self.server.listen(1)
        
        def wait_for_client():
            conn, addr = self.server.accept()
            self.client = conn
            self.connected = True
            self._start_listening()

        threading.Thread(target=wait_for_client, daemon=True).start()

    def join_game(self, ip, port=5555):
        """
        Thiết lập vai trò Máy khách (Client). Gửi yêu cầu kết nối đến địa chỉ IP Host.
        Trả về cờ (boolean) biểu thị sự thành công/thất bại của quá trình khởi tạo kết nối.
        """
        try:
            self.client.connect((ip, port))
            self.connected = True
            self._start_listening()
            return True
        except:
            return False

    def send_data(self, data):
        """
        Thực thi quá trình tuần tự hóa dữ liệu (Pickle) đối tượng Python và đóng gói 
        đẩy qua TCP socket với độ dài chuẩn 4 byte ở header nhằm ngăn chặn lỗi nối frame (TCP packet fragmentation).
        """
        if self.connected:
            try:
                serialized = pickle.dumps(data)
                # Gửi độ dài dữ liệu trước để tránh dính frame
                length = len(serialized).to_bytes(4, byteorder='big')
                self.client.sendall(length + serialized)
            except Exception as e:
                print("Lỗi gửi dữ liệu:", e)
                self.connected = False

    def _start_listening(self):
        """
        Khởi chạy tiến trình nền liên tục lắng nghe và bóc tách các byte dữ liệu.
        Dữ liệu nhận được sẽ được giải mã (unpickle) và đưa vào hàng đợi `received_data` an toàn với Lock.
        """
        def listen():
            while self.connected:
                try:
                    # Đọc 4 byte độ dài
                    length_bytes = self.client.recv(4)
                    if not length_bytes: break
                    length = int.from_bytes(length_bytes, byteorder='big')
                    
                    # Đọc đủ dữ liệu theo độ dài
                    data = b''
                    while len(data) < length:
                        packet = self.client.recv(length - len(data))
                        if not packet: break
                        data += packet
                        
                    obj = pickle.loads(data)
                    with self.lock:
                        self.received_data.append(obj)
                except:
                    self.connected = False
                    break
        threading.Thread(target=listen, daemon=True).start()

    def get_data(self):
        """
        Kiểm tra và truy xuất khối lượng dữ liệu khả dụng từ hàng đợi bản tin một cách tuần tự (FIFO).
        """
        with self.lock:
            if self.received_data:
                return self.received_data.pop(0)
            return None
            
    def close(self):
        """
        Đóng gói và dọn dẹp các luồng kết nối socket hiện có, đảm bảo giải phóng cổng mạng an toàn.
        """
        self.connected = False
        try: self.client.close()
        except: pass
        if self.server:
            try: self.server.close()
            except: pass
