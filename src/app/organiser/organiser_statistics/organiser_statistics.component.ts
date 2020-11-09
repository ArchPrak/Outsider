import {Component} from '@angular/core';
import { OrganiserService } from 'src/app/organiser.service';
import { HttpClient } from '@angular/common/http';
import * as CanvasJS from './canvasjs.min';
import { Router } from '@angular/router';

@Component({
  selector: 'org-statistics',
  templateUrl: 'organiser_statistics.component.html'
})

export class OrganiserStatistics {
  message: object;
  serverData: object;
  serverData1: object;
  constructor(private data1: OrganiserService, private httpClient: HttpClient, public router: Router) {
  }

  ngOnInit() {
    this.data1.currentMessage.subscribe((message) => this.message = message);
    console.log(this.data1.currentMessage);

    if(Object.keys(this.message).length == 0) {
      this.router.navigateByUrl('/login');
    }
    else {


    this.httpClient.post('http://127.0.0.1:5000/totalprofit', {'o_id': this.message['o_id']}).subscribe(data => {
      this.serverData = data as JSON;
      console.log(this.serverData);

      let chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        exportEnabled: true,
        title: {
          text: "Profit made per event"
        },
        data: [{
          type: "column",
          dataPoints: this.serverData
        }]
      });
      chart.render();
  });

  this.httpClient.post('http://127.0.0.1:5000/no_of_reg', {'o_id': this.message['o_id']}).subscribe(data => {
      this.serverData1 = data as JSON;
      console.log(this.serverData1);

      let chart1 = new CanvasJS.Chart("chartContainer1", {
        animationEnabled: true,
        exportEnabled: true,
        title: {
          text: "Number of registrations per event"
        },
        data: [{
          type: "column",
          dataPoints: this.serverData1
        }]
      });
      chart1.render();
  });
}
}
}
