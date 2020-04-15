import { Component, OnInit, NgZone, Output } from '@angular/core';
import { StudentService } from '../student.service';
import { EventEmitter } from '@angular/core';
import { OrganiserService } from '../organiser.service';
import {Router} from '@angular/router';
import { HttpClient } from '@angular/common/http';
import * as CanvasJS from './canvasjs.min';
@Component({
  templateUrl: './shome.component.html',
  styleUrls:['shome.component.css']
})

export class ShomeComponent implements OnInit {
  message: object;
  name: string;
  serverData: object;
  serverData2: JSON;
  serverData3: JSON;

  @Output() messageEvent = new EventEmitter();

  constructor(private student: StudentService, private ngZone: NgZone, public router: Router, private httpClient: HttpClient) {
    this.name = '';
  }

  ngOnInit() {
    this.student.currentMessage.subscribe(message => this.message = message);
    console.log(this.message);
    this.ngZone.run(() => {this.name = this.message['first_name'];});

    if(Object.keys(this.message).length == 0) {
      this.router.navigateByUrl('/login');
    } else{
      this.httpClient.post('http://127.0.0.1:5000/student/pie1', {'student_id': this.message['s_id']}).subscribe(data => {
        this.serverData2 = data as JSON;
        console.log(this.serverData2);


    let chart = new CanvasJS.Chart("chartContainer2", {
      theme: "light2",
      animationEnabled: true,
      exportEnabled: true,
      title:{
        text: "Popular event categories"
      },
      data: [{
        type: "pie",
        showInLegend: true,
        toolTipContent: "<b>{name}</b>: ${y} (#percent%)",
        indexLabel: "{name} - #percent%",

        dataPoints : this.serverData2
  }]
    });

    chart.render();
  });

  this.httpClient.get('http://127.0.0.1:5000/student/pie2').subscribe(data => {
        this.serverData3 = data as JSON;
        console.log(this.serverData3);


    let chart = new CanvasJS.Chart("chartContainer1", {
      theme: "light2",
      animationEnabled: true,
      exportEnabled: true,
      title:{
        text: "Popular Events"
      },
      data: [{
        type: "pie",
        showInLegend: true,
        toolTipContent: "<b>{name}</b>: ${y} (#percent%)",
        indexLabel: "{name} - #percent%",

        dataPoints : this.serverData3
  }]
    });

    chart.render();
  });




  }
  }

  get_events() {
    this.router.navigateByUrl('/dispevents');
    };
  add_hobby()
  {
    this.router.navigateByUrl('/addhobby');
  };
  reg_event()
  {
    this.router.navigateByUrl('/regevent');
  };
  get_prizes()
  {
    this.router.navigateByUrl('/dispprizes');
  };

  get_team()
  {
    this.router.navigateByUrl('/getteam');
  };

}
