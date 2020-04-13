import {Component} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router, Routes, RouterModule } from '@angular/router';
import { StudentService } from '../../student.service';




@Component({
  selector: 'all-event',
  templateUrl: './list_event.component.html'
})

export class DispEvents {
  message: object;
  serverData: object;
  past :String[];
  upcoming :String[];


  constructor(private httpClient: HttpClient, private data: StudentService, public router: Router) {

  }

  ngOnInit() {
    this.data.currentMessage.subscribe((message) => this.message = message);
    if(Object.keys(this.message).length == 0) {
      this.router.navigateByUrl('/login');
    }
    else {
      this.httpClient.post('http://127.0.0.1:5000/student/events', {'student_id': this.message['s_id']}).subscribe(data => {
        this.serverData = data as JSON;
         this.past=this.serverData["past"];
         this.upcoming=this.serverData["upcoming"];

      });
    };
  }


}
