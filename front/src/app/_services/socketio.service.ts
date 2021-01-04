import { io } from 'socket.io-client';
import {environment} from '@environments/environment';
import {Injectable} from '@angular/core';

export class SocketioService {
  socket;
  constructor() {   }
  setupSocketConnection() {
    this.socket = io(environment.apiUrl);
    // this.socket.emit('message', 'Hello there from Angular.');
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
