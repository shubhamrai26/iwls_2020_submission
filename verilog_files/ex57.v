module (ip_0,ip_1,ip_2,ip_3,ip_4,ip_5,ip_6,ip_7,ip_8,ip_9,ip_10,ip_11,ip_12,ip_13,ip_14,ip_15,ip_16,ip_17,ip_18,ip_19,ip_20,ip_21,ip_22,ip_23, o1);
input ip_0, ip_1, ip_2, ip_3, ip_4, ip_5, ip_6, ip_7, ip_8, ip_9, ip_10, ip_11, ip_12, ip_13, ip_14, ip_15, ip_16, ip_17, ip_18, ip_19, ip_20, ip_21, ip_22, ip_23;
output o1;
wire w_0, w_1, w_2, w_3, w_4, w_5, w_6, w_7, w_8, w_9, w_10, w_11, w_12;

assign w_0 = ip_22 & ip_23 & ip_6 & ip_7 & ~ip_5 ;
assign w_1 =  ip_11 & ip_22 & ip_6 & ip_7 & ~ip_3 & ~ip_5 ;
assign w_2 =  ip_11 & ip_3 & ip_6 & ip_7 & ~ip_16 & ~ip_5 ;
assign w_3 =  ip_16 & ip_22 & ip_23 & ip_6 & ~ip_3 & ~ip_5 ;
assign w_4 =  ip_16 & ip_22 & ip_6 & ~ip_11 & ~ip_3 & ~ip_5 ;
assign w_5 =  ip_11 & ip_16 & ip_23 & ip_3 & ip_6 & ~ip_5 & ~ip_7 ;
assign w_6 =  ip_16 & ip_6 & ~ip_11 & ~ip_22 & ~ip_5 & ~ip_7 ;
assign w_7 =  ip_16 & ip_22 & ip_3 & ip_6 & ~ip_23 & ~ip_5 & ~ip_7 ;
assign w_8 =  ip_16 & ip_23 & ip_3 & ip_6 & ~ip_11 & ~ip_22 & ~ip_5 ;
assign w_9 =  ip_22 & ip_3 & ip_6 & ~ip_11 & ~ip_16 & ~ip_5 & ~ip_7 ;
assign w_10 =  ip_16 & ip_6 & ~ip_22 & ~ip_23 & ~ip_3 & ~ip_5 & ~ip_7 ;
assign w_11 =  ip_6 & ip_7 & ~ip_11 & ~ip_22 & ~ip_23 & ~ip_3 & ~ip_5 ;
assign w_12 =  ip_11 & ip_23 & ip_6 & ~ip_16 & ~ip_22 & ~ip_3 & ~ip_5 & ~ip_7;
assign o1 = w_0 | w_1 | w_2 | w_3 | w_4 | w_5 | w_6 | w_7 | w_8 | w_9 | w_10 | w_11 | w_12;
endmodule
