module (ip_0,ip_1,ip_2,ip_3,ip_4,ip_5,ip_6,ip_7,ip_8,ip_9,ip_10,ip_11,ip_12,ip_13,ip_14,ip_15,ip_16,ip_17,ip_18,ip_19,ip_20,ip_21,ip_22, o1);
input ip_0, ip_1, ip_2, ip_3, ip_4, ip_5, ip_6, ip_7, ip_8, ip_9, ip_10, ip_11, ip_12, ip_13, ip_14, ip_15, ip_16, ip_17, ip_18, ip_19, ip_20, ip_21, ip_22;
output o1;
wire w_0, w_1, w_2, w_3, w_4, w_5, w_6, w_7, w_8;

assign w_0 = ip_2 ;
assign w_1 =  ip_3 ;
assign w_2 =  ip_5 ;
assign w_3 =  ~ip_1 ;
assign w_4 =  ~ip_14 & ~ip_8 ;
assign w_5 =  ip_11 & ip_17 & ~ip_8 ;
assign w_6 =  ip_17 & ~ip_11 & ~ip_14 ;
assign w_7 =  ip_11 & ip_14 & ip_8 & ~ip_17 ;
assign w_8 =  ~ip_11 & ~ip_17 & ~ip_8;
assign o1 = w_0 | w_1 | w_2 | w_3 | w_4 | w_5 | w_6 | w_7 | w_8;
endmodule
