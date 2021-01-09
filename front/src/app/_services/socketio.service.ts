import { io } from 'socket.io-client';
import {environment} from '@environments/environment';
import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class SocketioService {
  // @ts-ignore
  socketInstance: SocketIOClient.Socket;
  messages: Array<any>;
  constructor(private http: HttpClient) {}

  connect() {
    this.socketInstance = io(environment.apiUrl);
    this.socketInstance.emit('message', {data: 'Hello there from Angular.'});
  }

  iniServerSocket() {
    this.http.get(environment.apiUrl)
      .subscribe(data => {
      console.log(data);
      })
  }
}

// @Injectable({ providedIn: 'root' })
// export class SocketioService {
//       private socket;
//       constructor() {
//         this.socket = io(environment.apiUrl);
//       }

      // public sendMessage(message) {
      //   this.socket.emit('new-message', message);
      // }

      // public getMessages = () => {
      //   return Observable.create(observer => {
      //     this.socket.on('new-message', message => {
      //       observer.next(message);
      //     });
      //   });
      // };
// }
