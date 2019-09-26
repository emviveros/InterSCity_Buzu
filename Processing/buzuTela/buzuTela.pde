import oscP5.*;
import netP5.*;
PGraphics pg;
OscP5 oscP5;
float c, x, y,x1,y1, x2, y2, x3, y3;

void setup() {
  fullScreen();
  noCursor();
  //size(1000, 1000);
  oscP5 = new OscP5(this, 13000);
  pg = createGraphics(400, 400);
  
  //c = 1;
}

void draw() {
  
  fill(0, 55, 100, 1);
  rect(0, 0, width, height);
  
  fill(255);
  noStroke();
  ellipse(x, y, 2, 2);
  
  fill(255);
  noStroke();
  ellipse(x1, y1, 2, 2);
  
  fill(255);
  noStroke();
  ellipse(x2, y2, 2, 2);
  
  fill(255);
  noStroke();
  ellipse(x3, y3, 2, 2);
  
if (c>0){
  
  pg.beginDraw();
  pg.background(51);
  
  pg.fill(100);
  pg.stroke(100);
  pg.ellipse(x, y, 4, 4); 
  
  pg.fill(100);
  pg.stroke(100);
  pg.ellipse(x1, y1, 4, 4);
  
  pg.fill(100);
  pg.stroke(100);
  pg.ellipse(x2, y2, 4, 4);
  
  pg.fill(100);
  pg.stroke(100);
  pg.ellipse(x3, y3, 4, 4);
  
  pg.endDraw();
  }
  
  if (c<1){
  pg.beginDraw(); 
  fill(0, 55, 100, 80);
  rect(0, 0, width, height);
  pg.endDraw(); 
  }
}


void oscEvent(OscMessage theOscMessage) {
    if(theOscMessage.checkAddrPattern("/test")==true) {
    x = theOscMessage.get(0).floatValue();
    y = theOscMessage.get(1).floatValue();
  }
  if(theOscMessage.checkAddrPattern("/puts")==true){
    x1 = theOscMessage.get(0).floatValue();
    y1 = theOscMessage.get(1).floatValue();
}
if(theOscMessage.checkAddrPattern("/bean")==true){
    x2 = theOscMessage.get(0).floatValue();
    y2 = theOscMessage.get(1).floatValue();
}
if(theOscMessage.checkAddrPattern("/anus")==true){
    x3 = theOscMessage.get(0).floatValue();
    y3 = theOscMessage.get(1).floatValue();
}
    if(theOscMessage.checkAddrPattern("/clear")==true) {
    c = theOscMessage.get(0).floatValue();
}
println (x, y, x1, y1, x2, y2, x3, y3, c);
}
