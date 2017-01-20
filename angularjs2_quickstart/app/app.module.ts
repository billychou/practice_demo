import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent }  from './app.component';
import { ClickMeComponent } from './click-me.component';
import { KeyUpComponent_v1 } from './keyup.component';
import { LoopbackComponent } from './loop-back.component';
import { Logger } from './logger.service';

@NgModule({
  imports:      [ BrowserModule ],
  declarations: [ AppComponent, ClickMeComponent, KeyUpComponent_v1, LoopbackComponent ],
  bootstrap:    [ AppComponent, ClickMeComponent, KeyUpComponent_v1, LoopbackComponent ],
  providers: [ Logger ]
})
export class AppModule { }



