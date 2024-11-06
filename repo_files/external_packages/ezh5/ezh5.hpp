/* Written by Mengsu Chen mengsuchen@gmail.com
 * 
 * 
 *
 *
 *
 *
 */


#ifndef EZH5_H
#define EZH5_H

#include <hdf5.h>
#include <hdf5_hl.h>

// Preprocessor directives
// Please define EZH5_BOOST before including this file to force boost support
#ifdef EZH5_BOOST
#include <boost/numeric/ublas/vector.hpp>
#include <boost/numeric/ublas/matrix.hpp>
#endif

// Please define EZH5_EIGEN before including this file to force Eigen support
#ifdef EZH5_EIGEN
#include <Eigen/Core>
#endif


#include <complex>
#include <string>
#include <vector>
#include <cassert>


namespace ezh5{


	namespace trait {
		template<bool, typename T>
		struct enable_if{};

		template<typename T>
		struct enable_if<true, T>{
			typedef T type;
		};

		// for function operator=(T)
		template<typename T>
		struct is_scalar {
			static const bool value = false;
		};

		template<>
		struct is_scalar<int>{
			static const bool value = true;
		};

		template<>
		struct is_scalar<unsigned int>{
			static const bool value = true;
		};

		template<>
		struct is_scalar<long>{
			static const bool value = true;
		};

		template<>
		struct is_scalar<unsigned long>{
			static const bool value = true;
		};

		template<>
		struct is_scalar<float>{
			static const bool value = true;
		};

		template<>
		struct is_scalar<double>{
			static const bool value = true;
		};

		template<>
		struct is_scalar<std::complex<float> >{
			static const bool value = true;
		};

		template<>
		struct is_scalar<std::complex<double> >{
			static const bool value = true;
		};
	}//end name

	template<typename T>
	struct TypeMem{
		static hid_t id;
	};

	// define complex number datatype layout
	template<typename T>
	struct TypeMem<std::complex<T> >{
		static hid_t id;
		TypeMem(){
			H5Tinsert(id, "r", 0, TypeMem<T>::id);  // the name 'r' is to be compatible with h5py
			H5Tinsert(id, "i", sizeof(T), TypeMem<T>::id); // TODO: use HOFFSET
		}
	};

	// template<>
	// struct TypeMem<const char*>{
	// 	static hid_t id;
	// 	TypeMem(){
	// 	    H5Tset_size(id, H5T_VARIABLE);
	// 	}
	// };  // because the TypeFile<const char*> need to be H5T_FORTRAN_S1, so I use specialization in operator=() instead


	/// char* dsname
	template<typename T>
	hid_t write(hid_t loc_id, const char* dsname, const T& buf){
		hid_t dataspace_id = H5Screate(H5S_SCALAR);
		hid_t dataset_id = H5Dcreate(loc_id, dsname, TypeMem<T>::id, dataspace_id, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
		hid_t error_id = H5Dwrite(dataset_id, TypeMem<T>::id, H5S_ALL, H5S_ALL, H5P_DEFAULT, &buf);
		H5Dclose(dataset_id);
		H5Sclose(dataspace_id);
		return error_id;
	}

	/// string dsname
	template<typename T>
	hid_t write(hid_t loc_id, const std::string& dsname, const T& buf){
		return write(loc_id, dsname.c_str(), buf);
	}

	// /// char* dsname     // TODO: use enable_if to distinguish this from above
	// template<typename VEC>
	// hid_t write(hid_t loc_id, const char* dsname, const VEC& vec){
	// 	hsize_t dims[1];
	// 	dims[0] = vec.size();
	// 	hid_t dp_id = H5Screate_simple(1, dims, NULL);
	// 	hid_t ds_id = H5Dcreate(loc_id, dsname, TypeMem<VEC::value_type>::id, dp_id, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
	// 	hid_t err_id = H5Dwrite(ds_id, TypeMem<VEC::value_type>::id, H5S_ALL, H5S_ALL, H5P_DEFAULT, &vec[0]);
	// 	H5Dclose(ds_id);
	// 	H5Sclose(dp_id);
	// 	return err_id;
	// }
	// /// string dsname
	// template<typename VEC>
	// hid_t write(hid_t loc_id, const std::string& dsname, const VEC& vec){
	// 	return write(loc_id, dsname.c_str(), vec);
	// }


	/// write std::vector to hdf5
	/// char* dsname
	template<typename T>
	hid_t write(hid_t loc_id, const char* dsname, const std::vector<T>& vec){
		hsize_t dims[1];
		dims[0] = vec.size();
		//std::cout<<dsname<<std::endl;
		hid_t dp_id = H5Screate_simple(1, dims, NULL);
		assert(dp_id>=0);
		hid_t ds_id = H5Dcreate(loc_id, dsname, TypeMem<T>::id, dp_id, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
		assert(ds_id>=0);
		hid_t err_id = H5Dwrite(ds_id, TypeMem<T>::id, H5S_ALL, H5S_ALL, H5P_DEFAULT, &vec[0]);
		H5Dclose(ds_id);
		H5Sclose(dp_id);
		return err_id;
	}
	/// string dsname
	template<typename T>
	hid_t write(hid_t loc_id, const std::string& dsname, const std::vector<T>& vec){
		return write(loc_id, dsname.c_str(), vec);
	}

#ifdef _BOOST_UBLAS_VECTOR_
	/// char* dsname
	template<typename T>
	hid_t write(hid_t loc_id, const char* dsname, const boost::numeric::ublas::vector<T>& vec){
		hsize_t dims[1];
		dims[0] = vec.size();
		hid_t dp_id = H5Screate_simple(1, dims, NULL);
		hid_t ds_id = H5Dcreate(loc_id, dsname, TypeMem<T>::id, dp_id, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
		hid_t err_id = H5Dwrite(ds_id, TypeMem<T>::id, H5S_ALL, H5S_ALL, H5P_DEFAULT, &vec(0));
		H5Dclose(ds_id);
		H5Sclose(dp_id);
		return err_id;
	}

	/// string dsname
	template<typename T>
	hid_t write(hid_t loc_id, const std::string& dsname, const boost::numeric::ublas::vector<T>& vec){
		return write(loc_id, dsname.c_str(), vec);
	}
#endif


#ifdef _BOOST_UBLAS_MATRIX_
	template<typename T>
	hid_t write(hid_t loc_id, const char* dsname, const boost::numeric::ublas::matrix<T,
			boost::numeric::ublas::row_major>& mat){
		hsize_t dims[2];
		dims[0] = mat.size1();
		dims[1] = mat.size2();
		hid_t dp_id = H5Screate_simple(2, dims, NULL);
		htri_t is_exist = H5Lexists(loc_id, dsname, H5P_DEFAULT);
		hid_t ds_id = -1;
		switch (is_exist){
			case true:
				ds_id = H5Dopen1(loc_id, dsname);
				break;
			case false:
				ds_id = H5Dcreate(loc_id, dsname, TypeMem<T>::id, dp_id, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
				break;
			default:
				break;
		}
		assert(ds_id >=0);
		hid_t err_id = H5Dwrite(ds_id, TypeMem<T>::id, H5S_ALL, H5S_ALL, H5P_DEFAULT, &mat(0,0));
		assert(err_id>=0);
		H5Dclose(ds_id);
		H5Sclose(dp_id);
		return err_id;
	}
	/// string dsname
	template<typename T>
	hid_t write(hid_t loc_id, const std::string& dsname, const boost::numeric::ublas::matrix<T>& mat){
		return write(loc_id, dsname.c_str(), mat);
	}
#endif



//---------- read function    
	template<typename T>
	hid_t read(const hid_t loc_id, const char* dsname, T* p_buf){
		hid_t dataset_id = H5Dopen2(loc_id, dsname, H5P_DEFAULT);
		hid_t datatype_id = H5Dget_type(dataset_id);
		hid_t error_id = H5Dread(dataset_id, datatype_id, H5S_ALL, H5S_ALL, H5P_DEFAULT, p_buf);
		H5Dclose(dataset_id);
		return error_id;
	}


	// hid_t write_complex_vec(hid_t loc_id, const char* name, const std::size_t vec_size, const std::complex<double>* buf){
	// 	hsize_t dim=vec_size;
	// 	hid_t dataspace_id = H5Screate_simple(1, &dim, NULL);
	// 	hid_t dataset_id = H5Dcreate(loc_id, name, complex_tid, dataspace_id, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
	// 	hid_t error_id = H5Dwrite(dataset_id, complex_tid, H5S_ALL, H5S_ALL, H5P_DEFAULT, buf);
	// 	H5Dclose(dataset_id);
	// 	H5Sclose(dataspace_id);
	// 	return error_id;
	// }

	// hid_t read_complex(hid_t loc_id, const char* name, std::complex<double>* buf){
	// 	hid_t dataset_id = H5Dopen2(loc_id, name, H5P_DEFAULT);
	// 	hid_t datatype_id = H5Dget_type(dataset_id);
	// 	hid_t error_id = H5Dread(dataset_id, datatype_id, H5S_ALL, H5S_ALL, H5P_DEFAULT, buf);
	// 	H5Dclose(dataset_id);
	// 	return error_id;
	// }

}

namespace ezh5{

	// definition of class static variable
	template<> hid_t TypeMem<double>::id = H5T_NATIVE_DOUBLE;
	template<> hid_t TypeMem<float>::id = H5T_NATIVE_FLOAT;
	template<> hid_t TypeMem<int>::id = H5T_NATIVE_INT;
	template<> hid_t TypeMem<long>::id = H5T_NATIVE_LONG;
	template<> hid_t TypeMem<unsigned int>::id = H5T_NATIVE_UINT;
	template<> hid_t TypeMem<unsigned long>::id = H5T_NATIVE_ULONG;

	// hid_t TypeMem<const char*>::id =  H5Tcopy(H5T_C_S1);

	template<> hid_t TypeMem<std::complex<float> >::id = H5Tcreate(H5T_COMPOUND, sizeof(std::complex<float>));  // create compound datatype
	template<> hid_t TypeMem<std::complex<double> >::id = H5Tcreate(H5T_COMPOUND, sizeof(std::complex<double>));
	// TODO: why I need specification, instead of defining follow
	//template<typename T>
	//hid_t TypeMem<std::complex<T> >::id = H5Tcreate(H5T_COMPOUND, sizeof(std::complex<T>));


	TypeMem<std::complex<float> > obj_to_run_constructor_float;  // to add LAYOUT (STRUCTURE) to compound datatype
	TypeMem<std::complex<double> > obj_to_run_constructor_double;
	// TypeMem<char*> obj_to_run_constructor_charp;

}

namespace ezh5{

	class ID { // the base class for Node
	public:
		hid_t id;
		ID(): id(-1){}
		ID(hid_t id_in) : id(id_in){}

		~ID(){}

	};


	class Node :public ID{
	public:

		Node(){}

		Node(hid_t pid_in, const std::string& path_in)
				: ID(-1),
				  pid(pid_in),
				  path(path_in){
			//cout<<"creating "<<path<<endl;
		}


		Node& operator()(const std::string& path){
			return *this;
		}


		Node operator[](const std::string& path_more){
			if(this->id==-1){// in lazy
				htri_t is_exist = H5Lexists(pid, path.c_str(), H5P_DEFAULT);
				if (is_exist<0){
					assert(false);
				}else if (is_exist==false){
					this->id = H5Gcreate2(pid, path.c_str(), H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
				}else{
					this->id = H5Gopen(pid, path.c_str(), H5P_DEFAULT);
				}
			} // TODO: else open dataset, read, and return the value
			assert(this->id>=0);
			return Node(this->id, path_more);
		}


		/*HDF5 does not at this time provide a mechanism to remove a dataset
		 * from a file, or to reclaim the storage from deleted objects. Through
		 * the H5Gunlink function one can remove links to a dataset from the
		 * file structure. Once all links to a dataset have been removed, that
		 * dataset becomes inaccessible to any application and is effectively
		 * removed from the file. But this does not recover the space the
		 * dataset occupies.
		 *
		 * so the following will fail:
		 * fh5["aa"] = 1;
		 * fh5["aa"] = 2;
		 * *
		 * *
		 */


		/// write scalar
		template<typename T>
		typename trait::enable_if<trait::is_scalar<T>::value, Node>::type& operator=(T val){
			hid_t dataspace_id = -1;
			if(this->id == -1){
				htri_t is_exist = H5Lexists(pid, path.c_str(), H5P_DEFAULT);
				if (is_exist<0){
					assert(false);
				}else if (is_exist==false) {
					dataspace_id = H5Screate(H5S_SCALAR);
					this->id = H5Dcreate(pid, path.c_str(), TypeMem<T>::id, dataspace_id, H5P_DEFAULT, H5P_DEFAULT,
										 H5P_DEFAULT);
					assert(this->id>=0);
					hid_t error_id = H5Dwrite(id, TypeMem<T>::id, H5S_ALL, H5S_ALL, H5P_DEFAULT, &val);
					assert(error_id>=0);
					H5Dclose(this->id);
					H5Sclose(dataspace_id);
					this->id = -1;   // TODO: why keep on setting this->id here, not necessary
				}else{
					std::cout<<"dataset "<<path<<" already exists!"<<std::endl;
				}
			}
			return *this;
		}

		/// write std::vector
		template<typename T>
		Node& operator=(const std::vector<T>& vec){
			if(this->id == -1){
				htri_t is_exist = H5Lexists(pid, path.c_str(), H5P_DEFAULT);
				if (is_exist<0){
					assert(false);
				}else if (is_exist==false) {
					hsize_t dims[1];
					dims[0] = vec.size();
					hid_t dataspace_id = H5Screate_simple(1, dims, NULL);
					assert(dataspace_id >= 0);
					this->id = H5Dcreate(pid, path.c_str(), TypeMem<T>::id, dataspace_id, H5P_DEFAULT, H5P_DEFAULT,
										 H5P_DEFAULT);
					assert(this->id >=0);
					hid_t error_id = H5Dwrite(this->id, TypeMem<T>::id, H5S_ALL, H5S_ALL, H5P_DEFAULT, &vec[0]);
					assert(error_id>=0);
					H5Dclose(this->id);
					H5Sclose(dataspace_id);
					this->id = -1;
				}else{
					std::cout<<"dataset "<<path<<" already exists!"<<std::endl;
				}
			}
			return *this;
		}

		/// write boost::numeric::ublas::vector
#ifdef _BOOST_UBLAS_VECTOR_
		template<typename T>
		Node& operator=(const boost::numeric::ublas::vector<T>& vec){
			if(this->id == -1){
				htri_t is_exist = H5Lexists(pid, path.c_str(), H5P_DEFAULT);
				if (is_exist<0){
					assert(false);
				}else if (is_exist==false) {
					hsize_t dims[1];
					dims[0] = vec.size();
					hid_t dataspace_id = H5Screate_simple(1, dims, NULL);
					assert(dataspace_id >= 0);
					this->id = H5Dcreate(pid, path.c_str(), TypeMem<T>::id, dataspace_id, H5P_DEFAULT, H5P_DEFAULT,
										 H5P_DEFAULT);
					assert(this->id>=0);
					hid_t error_id = H5Dwrite(this->id, TypeMem<T>::id, H5S_ALL, H5S_ALL, H5P_DEFAULT, &vec(0));
					assert(error_id>=0);
					H5Dclose(this->id);
					H5Sclose(dataspace_id);
					this->id = -1;
				}else{
					std::cout<<"dataset "<<path<<" already exists!"<<std::endl;
				}
			}
			return *this;
		}
#endif

		/// write boost::numeric::ublas::vector
#ifdef _BOOST_UBLAS_MATRIX_
		template<typename T>
		Node& operator=(const boost::numeric::ublas::matrix<T,
				boost::numeric::ublas::row_major>& mat){
			hid_t dataspace_id = -1;
			if(this->id == -1){
				htri_t is_exist = H5Lexists(pid, path.c_str(), H5P_DEFAULT);
				if (is_exist<0) {
					assert(false);
				}else if (is_exist==false) {
					hsize_t dims[2];
					dims[0] = mat.size1();
					dims[1] = mat.size2();
					hid_t dataspace_id = H5Screate_simple(2, dims, NULL);
					assert(dataspace_id >= 0);
					this->id = H5Dcreate(this->pid, path.c_str(), TypeMem<T>::id, dataspace_id, H5P_DEFAULT,
										 H5P_DEFAULT, H5P_DEFAULT);
					hid_t error_id = H5Dwrite(this->id, TypeMem<T>::id, H5S_ALL, H5S_ALL, H5P_DEFAULT, &mat(0,0));
					assert(error_id>=0);
					H5Dclose(this->id);
					this->id = -1;
					H5Sclose(dataspace_id);
				}else{
					std::cout<<"dataset "<<path<<" already exists!"<<std::endl;
				}
			}
			return *this;
		}

		template<typename T>
		Node& operator=(const boost::numeric::ublas::matrix<T,
				boost::numeric::ublas::column_major>& mat_col_major){
			boost::numeric::ublas::matrix<T,
					boost::numeric::ublas::row_major> mat (mat_col_major); // convert to row_major for HDF5
			if(this->id == -1){
				htri_t is_exist = H5Lexists(pid, path.c_str(), H5P_DEFAULT);
				if (is_exist<0){
					assert(false);
				}else if (is_exist==false){
					hsize_t dims[2];
					dims[0] = mat.size1();
					dims[1] = mat.size2();
					hid_t dataspace_id = H5Screate_simple(2, dims, NULL);
					assert(dataspace_id>=0);
					this->id = H5Dcreate(this->pid, path.c_str(), TypeMem<T>::id, dataspace_id, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
					hid_t error_id = H5Dwrite(this->id, TypeMem<T>::id, H5S_ALL, H5S_ALL, H5P_DEFAULT, &mat(0,0));
					assert(error_id>=0);
					H5Dclose(this->id);
					this->id = -1;
					H5Sclose(dataspace_id);
				}else{
					std::cout<<"dataset "<<path<<" already exists!"<<std::endl;
				}
			}
			return *this;
		}


#endif


		// write Eigen::Matrix, Array
#ifdef EIGEN_EIGENBASE_H
		template<typename Derived>
        Node& operator=(const Eigen::EigenBase<Derived>& mat){
	    typedef typename Derived::Scalar _Scalar;
            hid_t dataspace_id = -1;
           if(this->id == -1){
               hsize_t dims[2];
               dims[0] = mat.rows();
               dims[1] = mat.cols();
               hid_t dataspace_id = H5Screate_simple(2, dims, NULL);
               assert(dataspace_id>=0);
               this->id = H5Dcreate(this->pid, path.c_str(), TypeMem<_Scalar>::id,
				    dataspace_id, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
           }
           hid_t error_id = H5Dwrite(this->id, TypeMem<_Scalar>::id,
				     H5S_ALL, H5S_ALL, H5P_DEFAULT, mat.derived().data());
           assert(error_id>=0);
           H5Dclose(this->id);
           this->id = -1;
           if (dataspace_id != -1) {H5Sclose(dataspace_id);}
            return *this;
        }
#endif


#ifdef EIGEN_BLOCK_H
		template<typename XprType, int BlockRows, int BlockCols, bool InnerPanel>
        Node& operator=(const Eigen::Block<XprType, BlockRows, BlockCols, InnerPanel>& mat){
            hid_t dataspace_id = -1;
            typedef typename XprType::Scalar Scalar;
            Scalar z (0.);
//            if(this->id == -1){
//                hsize_t dims[2];
//                dims[1] = mat.rows();
//                dims[0] = mat.cols();
//                hid_t dataspace_id = H5Screate_simple(2, dims, NULL);
//                assert(dataspace_id>=0);
//                this->id = H5Dcreate(this->pid, path.c_str(), TypeMem<_Scalar>::id, dataspace_id, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
//            }
//            hid_t error_id = H5Dwrite(this->id, TypeMem<_Scalar>::id, H5S_ALL, H5S_ALL, H5P_DEFAULT, mat.data());
//            assert(error_id>=0);
//            H5Dclose(this->id);
//            this->id = -1;
//            if (dataspace_id != -1) {H5Sclose(dataspace_id);}
            return *this;
        }
#endif

		Node& operator=(const char* str);
		Node& operator=(const std::string& str);


		~Node(){
			if(this->id>0){
				//cout<<"closing "<<path<<endl;
				H5Gclose(this->id);
				this->id = -1;
			}
		}

	public:
		hid_t pid; // parent_id
		std::string path;
	};


	Node& Node::operator=(const char* str){
		hid_t type_in_file = H5Tcopy(H5T_FORTRAN_S1);
		H5Tset_size(type_in_file, H5T_VARIABLE);
		hid_t type_in_mem = H5Tcopy(H5T_C_S1);
		H5Tset_size(type_in_mem, H5T_VARIABLE);

		hid_t dataspace_id = -1;
		if(this->id == -1){
			// hsize_t dims[1] = {1};
			dataspace_id = H5Screate(H5S_SCALAR);
			this->id = H5Dcreate(pid, path.c_str(), type_in_mem, dataspace_id, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
		}
		hid_t error_id = H5Dwrite(id, type_in_mem, H5S_ALL, H5S_ALL, H5P_DEFAULT, &str);
		H5Dclose(this->id);
		this->id = -1;
		if (dataspace_id != -1) {H5Sclose(dataspace_id);}
		H5Tclose(type_in_file);
		H5Tclose(type_in_mem);
		return *this;
	}


	Node& Node::operator=(const std::string& str){
		return operator=(str.c_str());
	}

	class Dataset : public Node{
	};


	class File : public Node{
	public:
		// TODO: open an opened file
		// TODO: implement open if exists, create if not
		File(const std::string& path, unsigned flags)
				: __auto_close(true){
			if(flags==H5F_ACC_RDWR || flags==H5F_ACC_RDONLY){
				this->id = H5Fopen(path.c_str(), flags, H5P_DEFAULT);
			}else if (flags==H5F_ACC_TRUNC || flags==H5F_ACC_EXCL){
				this->id = H5Fcreate(path.c_str(), flags, H5P_DEFAULT, H5P_DEFAULT);
			}else{
				assert(!"unknow file access mode");
			}
		}

		/// a special constructor to construct File from an exiting file id
		/// this constructor should only be used for low level code to avoid confusing
		File(hid_t fid)
				: __auto_close(false){
			this->id = fid;
		}

		~File(){
			if (__auto_close && this->id !=-1) {
				H5Fclose(this->id);
			}
			this->id = -1;  // so that ~Node will not try to close it again
		}
	private:
		bool __auto_close;
	};
}

#include <iostream>
namespace ezh5 {
	std::string& operator<<(std::string& str, ezh5::Node& node){ // TODO: doesn't work, maybe because the file string type is H5T_S_C
        hid_t dataset_id = H5Dopen2(node.pid, node.path.c_str(), H5P_DEFAULT); assert(dataset_id>=0);
        hid_t datatype_id = H5Dget_type(dataset_id); assert(datatype_id>=0);
        std::size_t sdim = H5Tget_size(datatype_id);
        str.resize(sdim);
        std::cout<<sdim<<std::endl;
        hid_t error_id = H5Dread(dataset_id, datatype_id, H5S_ALL, H5S_ALL, H5P_DEFAULT, &str[0]);
        assert(error_id>=0);
        H5Dclose(dataset_id);

		return str;
	}

    template<typename T>
    typename ezh5::trait::enable_if<trait::is_scalar<T>::value, T>::type& operator<<(T& data, const ezh5::Node& node){
        ezh5::read(node.pid, node.path.c_str(), &data);
        return data;
    }


    template<typename T>
    void operator<<(std::vector<T>& vec, const ezh5::Node& node){
        hid_t dataset_id = H5Dopen2(node.pid, node.path.c_str(), H5P_DEFAULT);
        hid_t datatype_id = H5Dget_type(dataset_id);
        hid_t dataspace_id = H5Dget_space(dataset_id);
        hsize_t dims[1];
        int err = H5Sget_simple_extent_dims(dataspace_id,dims,NULL); assert(err>=0);
        if (dims[0]>0) {
            vec.resize(dims[0]);
            hid_t error_id = H5Dread(dataset_id, datatype_id, H5S_ALL, H5S_ALL, H5P_DEFAULT, &vec[0]);
        }
    }


#ifdef _BOOST_UBLAS_VECTOR_
    template<typename T>
    void operator<<(boost::numeric::ublas::vector<T>& vec, const ezh5::Node& node){
        hid_t dataset_id = H5Dopen2(node.pid, node.path.c_str(), H5P_DEFAULT);
        hid_t datatype_id = H5Dget_type(dataset_id);
        hid_t dataspace_id = H5Dget_space(dataset_id);
        hsize_t dims[1];
        int err = H5Sget_simple_extent_dims(dataspace_id,dims,NULL); assert(err>=0);
        if (dims[0]>0) {
            vec.resize(dims[0]);
            hid_t error_id = H5Dread(dataset_id, datatype_id, H5S_ALL, H5S_ALL, H5P_DEFAULT, &vec(0));
        }
    }


#endif


}


#endif
