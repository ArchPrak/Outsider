import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable()
export class StudentService {
  private messageSource = new BehaviorSubject({});
  currentMessage = this.messageSource.asObservable();

  constructor() {

  }

  changeMessage(message: object) {
    //console.log(message);
    this.messageSource.next(message);
  }

}
