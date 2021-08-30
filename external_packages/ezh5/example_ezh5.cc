#include <boost/numeric/ublas/vector.hpp>
#include "ezh5.hpp"
#include <complex>
#include <vector>

int main(){
    ezh5::File f ("del_example_ezh5.h5", H5F_ACC_TRUNC);  // create a file object called f
    f["length unit"] = "meter";
    f["time unit"] = "second";
    f["light speed"] = 3.0e8;
    f["solar system"]["mass unit"] = "kg";
    f["solar system"]["earth"]["mass"] = 5.972e24;

    f["distances to sun"] = (std::vector<int> {1, 200, 8, 3, 6});

    boost::numeric::ublas::vector<std::complex<double> > ublas_vec (4);
    ublas_vec[0] = std::complex<double> (3, 6);
    ublas_vec[1] = 3;
    ublas_vec[2] = 5;
    ublas_vec[3] = 9;
    f["a ublas vector"] = ublas_vec;

    //ezh5::Node myhome = f["solar system"]["earth"];
    //myhome["population"] = 157893294;  // why doesn't work here
    // std::vector<int> x(3);
    // fh5["vec"] = x;

    // fh5["group"]["y"] = 0.1;
    // fh5["group"]["subgroup"]["z"] = 0.2;
    // ezh5::Node gr= fh5["group2"];
    // gr["x2"] = 0.5;
    // gr["y2"] = std::complex<double> (1.2, 3.5);


    f.~File();

    ezh5::File g ("del_example_ezh5.h5", H5F_ACC_RDONLY);  // create a file object called f
//    std::string name;
//    name<<g["length unit"];
//    std::cout<<name<<std::endl;

    //hid_t fid = H5Fopen("del_example_ezh5.h5", H5F_ACC_RDONLY,  H5P_DEFAULT);
    char buf[20];
    double speed=0.;
    //speed<<g["light speed"];
    speed<<g["solar system"]["earth"]["mass"];
    //ezh5::read(fid, "light speed", &speed);
    std::cout<<speed<<std::endl;

    std::vector<int> distances;
    distances<<g["distances to sun"];
    for(int i=0; i<distances.size(); ++i){
        std::cout<<distances[i]<<std::endl;
    }

    boost::numeric::ublas::vector<std::complex<double> > std_vec;
    std_vec<<g["a ublas vector"];
    for(int i=0; i<std_vec.size(); ++i){
        std::cout<<std_vec[i]<<std::endl;
    }

//    hid_t dset = H5Dopen(fid, "length unit", H5P_DEFAULT);
//    hid_t  filetype = H5Dget_type (dset);
//    std::size_t sdim = H5Tget_size (filetype);
//    sdim++;                         /* Make room for null terminator */
//
//    hid_t memtype = H5Tcopy (H5T_C_S1);
//    herr_t status = H5Tset_size (memtype, H5T_VARIABLE);
//
//    /*
//     * Read the data.
//     */
//    status = H5Dread (dset, memtype, H5S_ALL, H5S_ALL, H5P_DEFAULT, &buf);
//
//
//    printf("%s", &buf);

    return 0;
}
