module (ip_0,ip_1,ip_2,ip_3,ip_4,ip_5,ip_6,ip_7,ip_8,ip_9,ip_10,ip_11,ip_12,ip_13,ip_14,ip_15, o1);
input ip_0, ip_1, ip_2, ip_3, ip_4, ip_5, ip_6, ip_7, ip_8, ip_9, ip_10, ip_11, ip_12, ip_13, ip_14, ip_15;
output o1;
wire w_0, w_1;

assign w_0 = ip_15 & ~ip_7 ;
assign w_1 =  ip_7 & ~ip_15;
assign o1 = w_0 | w_1;
endmodule
