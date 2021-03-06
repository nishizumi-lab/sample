//Simulate of 2nd system with two 1st systems
s=%s;
t=0:0.01:10;
G=10/((s+5)*(s+2));
C=1+1/(0.072*s);sys=syslin("c",G*C/(1+G*C));
y1=csim("step",t,sys);
C=1+1/(1*s);sys=syslin("c",G*C/(1+G*C));
y2=csim("step",t,sys);
C=1+1/(3*s);sys=syslin("c",G*C/(1+G*C));
y3=csim("step",t,sys);
clf(); plot2d(t',[y1',y2',y3'])
