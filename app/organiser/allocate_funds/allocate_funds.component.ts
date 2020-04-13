import {Component, Inject} from '@angular/core';
import {MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';

@Component({
  selector: 'fund-allocate-form',
  templateUrl: 'allocate_funds.component.html',
})

export class DialogOverviewExampleDialog {
  amount:number;
  constructor(public dialogRef: MatDialogRef<DialogOverviewExampleDialog>) {
  }

  onClick() {
    console.log(this.amount);
    this.dialogRef.close();
  }

  onNoClick() {
    this.dialogRef.close();
  }
}
