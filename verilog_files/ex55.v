module (ip_0,ip_1,ip_2,ip_3,ip_4,ip_5,ip_6,ip_7,ip_8,ip_9,ip_10,ip_11,ip_12,ip_13,ip_14,ip_15,ip_16,ip_17,ip_18,ip_19,ip_20,ip_21,ip_22,ip_23,ip_24,ip_25,ip_26,ip_27,ip_28,ip_29,ip_30,ip_31,ip_32,ip_33,ip_34,ip_35,ip_36,ip_37,ip_38,ip_39,ip_40,ip_41, o1);
input ip_0, ip_1, ip_2, ip_3, ip_4, ip_5, ip_6, ip_7, ip_8, ip_9, ip_10, ip_11, ip_12, ip_13, ip_14, ip_15, ip_16, ip_17, ip_18, ip_19, ip_20, ip_21, ip_22, ip_23, ip_24, ip_25, ip_26, ip_27, ip_28, ip_29, ip_30, ip_31, ip_32, ip_33, ip_34, ip_35, ip_36, ip_37, ip_38, ip_39, ip_40, ip_41;
output o1;
wire w_0, w_1, w_2, w_3, w_4, w_5, w_6, w_7, w_8;

assign w_0 = ip_11 & ip_30 & ip_36 & ~ip_12 ;
assign w_1 =  ip_11 & ip_30 & ~ip_1 & ~ip_34 ;
assign w_2 =  ip_11 & ip_30 & ~ip_18 & ~ip_36 ;
assign w_3 =  ip_1 & ip_11 & ip_18 & ip_30 & ~ip_20 ;
assign w_4 =  ip_1 & ip_11 & ip_20 & ip_30 & ~ip_18 ;
assign w_5 =  ip_11 & ip_12 & ip_18 & ip_30 & ~ip_1 ;
assign w_6 =  ip_11 & ip_20 & ip_30 & ip_34 & ~ip_12 ;
assign w_7 =  ip_11 & ip_12 & ip_30 & ~ip_1 & ~ip_20 ;
assign w_8 =  ip_11 & ip_12 & ip_30 & ~ip_34 & ~ip_36;
assign o1 = w_0 | w_1 | w_2 | w_3 | w_4 | w_5 | w_6 | w_7 | w_8;
endmodule
