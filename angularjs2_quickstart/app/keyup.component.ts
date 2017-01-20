/**
 * Created by songchuanzhou on 17/1/12.
 */

import  { Component } from '@angular/core';

@Component({
  selector: 'keyup',
  templateUrl: "keyup.html"
})


export class KeyUpComponent_v1 {
  values = '';
  //传入event事件对象
  onKey(event:any) { //without type info
    this.values += event.target.value + ' | ';
  }
}

