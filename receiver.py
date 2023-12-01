import colors

class ReceiverProcess:
    """ Represent the receiver process in the application layer  """
    __buffer = list()
    #lock keyword
    @staticmethod
    def deliver_data(data):
        """ deliver data from the transport layer RDT receiver to the application layer
        :param data: a character received by the RDT RDT receiver
        :return: no return value
        """
        ReceiverProcess.__buffer.append(data)
        print (ReceiverProcess.__buffer)
        return

    @staticmethod
    def get_buffer():
        """ To get the message the process received over the network
        :return:  a python list of characters represent the incoming message
        """
        return ReceiverProcess.__buffer


class RDTReceiver:
    """" Implement the Reliable Data Transfer Protocol V2.2 Receiver Side """
    
    def __init__(self):
        self.sequence = '0'

    @staticmethod
    def is_corrupted(packet):
        """ Check if the received packet from sender is corrupted or not
            :param packet: a python dictionary represent a packet received from the sender
            :return: True -> if the reply is corrupted | False ->  if the reply is NOT corrupted
        """
        if packet['checksum'] == ord(str(packet['data'])):
            return False
        else:
            print(colors.cred + 'Receiver: Incorrect checksum' + colors.cend)
            return True

    @staticmethod
    def is_expected_seq(rcv_pkt, exp_seq):
        """ Check if the received reply from receiver has the expected sequence number
         :param rcv_pkt: a python dictionary represent a packet received by the receiver
         :param exp_seq: the receiver expected sequence number '0' or '1' represented as a character
         :return: True -> if ack in the reply match the   expected sequence number otherwise False
        """
        if rcv_pkt['sequence_number'] == exp_seq:
            return True
        else:
            print(colors.cred + 'Receiver: Incorrect sequence number' + colors.cend)
            return False

    @staticmethod
    def make_reply_pkt(seq, checksum):
        """ Create a reply (feedback) packet with to acknowledge the received packet
        :param seq: the sequence number '0' or '1' to be acknowledged
        :param checksum: the checksum of the ack the receiver will send to the sender
        :return:  a python dictionary represent a reply (acknowledgement)  packet
        """
        reply_pck = {
            'ack': seq,
            'checksum': checksum
        }
        return reply_pck

    def rdt_rcv(self, rcv_pkt):
        
        """  Implement the RDT v2.2 for the receiver
        :param rcv_pkt: a packet delivered by the network layer 'udt_send()' to the receiver
        :return: the reply packet
        """
        
        print(colors.cblue + f'Receiver expected seq number: {self.sequence}' + colors.cend)
        print(colors.cblue + f'Receiver received: {rcv_pkt}' + colors.cend)

        ack = self.sequence
        if self.is_corrupted(rcv_pkt) or not self.is_expected_seq(rcv_pkt, self.sequence):
            match ack:
                case '0':
                    ack = '1'
                case '1':
                    ack = '0'
            reply_pkt = self.make_reply_pkt(ack, ord(str(ack)))
            print(colors.cblue + f'Receiver is sending: {reply_pkt}' + colors.cend)
            return reply_pkt

        else:
            match self.sequence:
                case '0':
                    self.sequence = '1'
                case '1':
                    self.sequence = '0'

            ReceiverProcess.deliver_data(rcv_pkt['data'])

            reply_pkt = self.make_reply_pkt(ack, ord(str(ack)))
            print(colors.cblue + f'Receiver is sending: {reply_pkt}' + colors.cend)
            return reply_pkt
        
