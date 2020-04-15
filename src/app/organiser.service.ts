import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable()
export class OrganiserService {
  private messageSource = new BehaviorSubject({});
  currentMessage = this.messageSource.asObservable();

  constructor() {

  }

  changeMessage(message: object) {
    this.messageSource.next(message);
  }

}
