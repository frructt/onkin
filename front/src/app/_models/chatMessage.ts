export class ChatMessageDto {
    username: string;
    msg: string;
    roomId: string;
    timestamp: string;

    constructor(username: string, msg: string, roomId: string, timestamp: string) {
        this.username = username;
        this.msg = msg;
        this.roomId = roomId;
        this.timestamp = timestamp;
    }
}
