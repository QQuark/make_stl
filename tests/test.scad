
module box(w,d,h) // AUTO_MAKE_STL[1:2][2:10][1]
{
    cube([w,d,h]);
}

module label(s,t) // AUTO_MAKE_STL[2,5]["test1","test2"]
{
    translate([0, 0, 0.4]) linear_extrude(1) text(t, s, halign="center", valign="center");
    cube([s*5,s*2,1], center = true);
}

%label(5, "test2");


