export class ChatMessageDto {
    username: string;
    msg: string;
    timestamp: string;

    constructor(username: string, msg: string, timestamp: string) {
        this.username = username;
        this.msg = msg;
        this.timestamp = timestamp;
    }
}
